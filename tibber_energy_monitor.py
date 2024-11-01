import tibber
import time
import paho.mqtt.client as mqtt
import os
import json
import random
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get configurations from environment variables
tibber_token = os.getenv("TIBBER_TOKEN")
mqtt_broker = os.getenv("MQTT_BROKER")
mqtt_username = os.getenv("MQTT_USERNAME")
mqtt_password = os.getenv("MQTT_PASSWORD")

# Set up MQTT client
client_id = f'tibber-api-{random.randint(0, 1000)}'
client = mqtt.Client(client_id=client_id, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(mqtt_username, mqtt_password)

# Connect to MQTT broker
client.connect(mqtt_broker, 1883, 60)
client.loop_start()

# Home Assistant MQTT Discovery configuration
def publish_config(sensor_name, unit, icon):
    config_topic = f"homeassistant/sensor/tibber_{sensor_name}/config"
    config = {
        "name": f"Tibber {sensor_name.capitalize()} Prijs",
        "state_topic": f"tibber/{sensor_name}",
        "unit_of_measurement": unit,
        "value_template": "{{ value | float }}",
        "icon": icon,
        "unique_id": f"tibber_{sensor_name}_price",
        "device": {
            "identifiers": ["tibber_energy_monitor"],
            "name": "Tibber Energy Monitor",
            "model": "Custom Tibber Integration",
            "manufacturer": "Custom"
        },
        "device_class": "monetary",
        "state_class": "measurement"
    }
    client.publish(config_topic, json.dumps(config), retain=True)
    logging.info(f"Published config for {sensor_name}")

# Publish configurations for discovery
publish_config("energie", "EUR/kWh", "mdi:flash")
publish_config("belasting", "EUR/kWh", "mdi:cash")
publish_config("totaal", "EUR/kWh", "mdi:cash-multiple")

def publish_price(base_topic, sensor_name, value):
    formatted_value = f"{value:.5f}"
    topic = f"{base_topic}/{sensor_name}"
    client.publish(topic, formatted_value, retain=True)
    logging.info(f"Published {topic}: {formatted_value}")

def wait_until_next_5min_interval():
    now = datetime.now()
    minutes_to_next = 5 - (now.minute % 5)
    next_run = now + timedelta(minutes=minutes_to_next)
    next_run = next_run.replace(second=0, microsecond=0)
    wait_seconds = (next_run - now).total_seconds()
    time.sleep(wait_seconds)

while True:
    try:
        # Create new connection each time
        account = tibber.Account(tibber_token)
        home = account.homes[1]
        
        current_subscription = home.current_subscription
        
        if current_subscription and current_subscription.price_info:
            current_price = current_subscription.price_info.current
            
            if current_price:
                subscription_energy = current_price.energy
                subscription_total = current_price.total
                subscription_tax = current_price.tax

                logging.info(f"Energieprijs: {subscription_energy}")
                logging.info(f"Belasting: {subscription_tax}")
                logging.info(f"Totaal: {subscription_total}")

                # Publish values to MQTT broker
                base_topic = "tibber"
                publish_price(base_topic, "energie", subscription_energy)
                publish_price(base_topic, "belasting", subscription_tax)
                publish_price(base_topic, "totaal", subscription_total)
            else:
                logging.warning("Geen huidige prijsinformatie beschikbaar.")
        else:
            logging.warning("Geen huidige abonnementsinformatie of prijsinformatie beschikbaar.")
    except Exception as e:
        logging.error(f"Er is een fout opgetreden: {e}")
    
    wait_until_next_5min_interval()
# werkend

