import json
import paho.mqtt.client as mqtt
from pathlib import Path
from mysql_db_manager import MySqlDbManager
from plugins.cnc_plugin_interface import CncPlugin
import importlib
import sys

class MQTTReader:
    def __init__(self, broker='broker.emqx.io', port=1883, topic='sensor/CNC', class_config_file='cnc_classes.json', plugins_dir='plugins'):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.class_map = self.load_class_config(class_config_file)
        self.plugins_dir = Path(plugins_dir)
        sys.path.insert(0, str(self.plugins_dir.resolve()))  # Add plugins dir to sys.path

        self.db_manager = MySqlDbManager()

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def load_class_config(self, filepath):
        try:
            with open(filepath, 'r') as f:
                config = json.load(f)
            return {item['cnc_id']: item['class_name'] for item in config}
        except Exception as e:
            print(f"[ERROR] Failed to load class config: {e}")
            return {}

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"[INFO] Connected to MQTT Broker: {self.broker}")
            client.subscribe(self.topic)
            print(f"[INFO] Subscribed to topic: {self.topic}")
        else:
            print(f"[ERROR] Failed to connect, return code {rc}")

    def on_message(self, client, userdata, msg):
        try:
            payload_str = msg.payload.decode()
            data = json.loads(payload_str)

            required_fields = ['cnc_id', 'part_program', 'timestamp', 'payload']
            if not all(k in data for k in required_fields):
                print(f"[ERROR] Missing required fields in message: {payload_str}")
                return

            if not isinstance(data['payload'], dict):
                print(f"[ERROR] 'payload' field is not a JSON object: {payload_str}")
                return

            cnc_id = data['cnc_id']
            class_name = self.class_map.get(cnc_id)

            if not class_name:
                print(f"[ERROR] No class mapped for cnc_id '{cnc_id}'")
                return

            try:
                module = importlib.import_module(class_name)
                cls = getattr(module, class_name)
                instance = cls(data, self.db_manager)
                # instance = cls(data, self.db_manager)
                # Optionally: do something with instance here.. 
            except Exception as e:
                print(f"[ERROR] Failed to import or instantiate '{class_name}': {e}")

        except json.JSONDecodeError:
            print(f"[ERROR] Invalid JSON: {msg.payload.decode()}")
        except Exception as e:
            print(f"[ERROR] Exception processing message: {e}")

    def start(self):
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_forever()
        except Exception as e:
            print(f"[ERROR] {e}")
