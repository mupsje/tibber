import tibber
import time
import paho.mqtt.client as mqtt
import os
import json
import logging

# Configureer logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Verkrijg de configuraties uit de omgevingsvariabelen
tibber_token = os.getenv("TIBBER_TOKEN")
mqtt_broker = os.getenv("MQTT_BROKER")
mqtt_username = os.getenv("MQTT_USERNAME")
mqtt_password = os.getenv("MQTT_PASSWORD")

# MQTT-client instellen
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(mqtt_username, mqtt_password)

# Verbinden met de MQTT-broker
client.connect(mqtt_broker, 1883, 60)
client.loop_start()

# Home Assistant MQTT Discovery configuratie
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

# Publiceer configuraties voor discovery
publish_config("energie", "EUR/kWh", "mdi:flash")
publish_config("belasting", "EUR/kWh", "mdi:cash")
publish_config("totaal", "EUR/kWh", "mdi:cash-multiple")

def publish_price(topic, value):
    formatted_value = f"{value:.5f}"
    client.publish(topic, formatted_value, retain=True)
    logging.info(f"Published {topic}: {formatted_value}")

def fetch_and_publish_prices():
    try:
        # Maak een nieuwe Tibber-verbinding voor elke update
        account = tibber.Account(tibber_token)
        home = account.homes[1]
        
        current_price = home.current_subscription.price_info.current
        
        if current_price:
            subscription_energy = current_price.energy
            subscription_total = current_price.total
            subscription_tax = current_price.tax

            logging.info(f"Energieprijs: {subscription_energy}")
            logging.info(f"Belasting: {subscription_tax}")
            logging.info(f"Totaal: {subscription_total}")

            # Publiceer de waarden naar de MQTT-broker
            publish_price("tibber/energie", subscription_energy)
            publish_price("tibber/belasting", subscription_tax)
            publish_price("tibber/totaal", subscription_total)
        else:
            logging.warning("Geen huidige prijsinformatie beschikbaar.")
    except Exception as e:
        logging.error(f"Er is een fout opgetreden bij het ophalen of publiceren van prijzen: {e}")

# Hoofdlus
while True:
    fetch_and_publish_prices()
    time.sleep(300)  # Wacht 5 minuten
