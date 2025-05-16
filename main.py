from mqtt_reader import MQTTReader

if __name__ == "__main__":
    reader = MQTTReader(
        broker="broker.emqx.io",
        topic="sensor/CNC",
        class_config_file="cnc_classes.json",
        plugins_dir="plugins"
    )
    reader.start()
