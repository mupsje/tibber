import paho.mqtt.client as mqtt
import os
import random
import logging
from dotenv import load_dotenv

load_dotenv()

class MqttClient:
    def __init__(self):
        self.mqtt_broker = os.getenv("MQTT_BROKER")
        self.mqtt_username = os.getenv("MQTT_USERNAME")
        self.mqtt_password = os.getenv("MQTT_PASSWORD")
        
        if not all([self.mqtt_broker, self.mqtt_username, self.mqtt_password]):
            raise ValueError("Missing required MQTT configuration")

        client_id = f'tibber-{random.randint(0, 1000)}'
        self.client = mqtt.Client(client_id=client_id, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        self.client.username_pw_set(self.mqtt_username, self.mqtt_password)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.mqtt_broker, 1883, 60)
            self.client.loop_start()
        except Exception as e:
            logging.error(f"Failed to connect to MQTT broker: {e}")
            raise

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            logging.info("Connected to MQTT broker")
        else:
            logging.error(f"Failed to connect to MQTT broker with code {rc}")

    def on_disconnect(self, client, userdata, rc):
        logging.warning("Disconnected from MQTT broker")
        if rc != 0:
            self.connect()

    def publish(self, topic, message, retain=False):
        try:
            result = self.client.publish(topic, message, retain=retain)
            if result.rc != 0:
                logging.error(f"Failed to publish message: {result.rc}")
        except Exception as e:
            logging.error(f"Error publishing message: {e}")

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
