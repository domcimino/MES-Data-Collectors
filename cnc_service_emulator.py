import paho.mqtt.client as mqtt
import time
import json

BROKER = 'broker.emqx.io'
PORT = 1883
TOPIC = 'sensor/CNC'
SAMPLE_DATA_FILE = 'sample_data.json'
DELAY_SECONDS = 2  # Time between each publish

def load_sample_data(filepath):
    try:
        with open(filepath, 'r') as f:
            return [json.loads(line.strip()) for line in f if line.strip()]
    except Exception as e:
        print(f"[ERROR] Failed to load sample data: {e}")
        return []

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[INFO] Connected to MQTT broker")
    else:
        print(f"[ERROR] Failed to connect. Code: {rc}")

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(BROKER, PORT, 60)
    client.loop_start()

    data = load_sample_data(SAMPLE_DATA_FILE)
    if not data:
        return

    for entry in data:
        payload = json.dumps(entry)
        client.publish(TOPIC, payload)
        print(f"[PUBLISHED] {payload}")
        time.sleep(DELAY_SECONDS)

    client.loop_stop()
    client.disconnect()
    print("[INFO] Done publishing sample data.")

if __name__ == '__main__':
    main()
