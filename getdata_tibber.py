import tibber
import time
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os
import json

# Laad omgevingsvariabelen uit het .env bestand
load_dotenv()

# Verkrijg de configuraties uit de omgevingsvariabelen
tibber_token = os.getenv("TIBBER_TOKEN")
mqtt_broker = os.getenv("MQTT_BROKER")
mqtt_username = os.getenv("MQTT_USERNAME")
mqtt_password = os.getenv("MQTT_PASSWORD")

# Tibber-account instellen
account = tibber.Account(tibber_token)
home = account.homes[1]

# MQTT-client instellen met specifieke Callback API versie
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
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

# Publiceer configuraties voor discovery
publish_config("energie", "EUR/kWh", "mdi:flash")
publish_config("belasting", "EUR/kWh", "mdi:cash")
publish_config("totaal", "EUR/kWh", "mdi:cash-multiple")

while True:
    current_subscription = home.current_subscription
    
    if current_subscription and current_subscription.price_info:
        current_price = current_subscription.price_info.current
        
        if current_price:
            subscription_energy = current_price.energy
            subscription_total = current_price.total
            subscription_tax = current_price.tax

            print(f"Energieprijs: {subscription_energy}")
            print(f"Belasting: {subscription_tax}")
            print(f"Totaal: {subscription_total}")
            print()

            # Publiceer de waarden naar de MQTT-broker
            client.publish("tibber/energie", subscription_energy)
            client.publish("tibber/belasting", subscription_tax)
            client.publish("tibber/totaal", subscription_total)
        else:
            print("Geen huidige prijsinformatie beschikbaar.")
    else:
        print("Geen huidige abonnementsinformatie of prijsinformatie beschikbaar.")
    
    # Wacht 5 minuten (300 seconden)
    time.sleep(300)

# Stop de MQTT-loop (optioneel, als je dit zou willen afsluiten)
# client.loop_stop()
# client.disconnect()
