# Tibber Energy Monitor

![image](https://github.com/user-attachments/assets/cebf20b4-8faf-49dc-af22-5037e43794dc)

Deze applicatie haalt real-time energieprijzen op van Tibber en publiceert ze naar Home Assistant via MQTT.
Ik wil graag de kale prijs in Hassio hebben om de zonnepanelen uit te schakelen wanneer de prijs in de min is. (negatief)
Nu zien wij enkel alleen de prijs inclusief belasting, en daar hebben we niks aan.

## Functionaliteiten
- Real-time energieprijzen van Tibber
- Automatische integratie met Home Assistant via MQTT discovery
- Prijsupdates elke 5 minuten
- SSH toegang voor beheer
- Draait in Docker container

## Vereisten
- Docker en Docker Compose
- Tibber account en API token
- MQTT broker (bijvoorbeeld Mosquitto)
- Home Assistant

## Installatie

1. Clone de repository:
```
git clone https://github.com/[jouw-username]/tibber-energy-monitor
```
2. Maak een .env bestand aan met de volgende inhoud:
```
TIBBER_TOKEN=jouw_tibber_token
MQTT_BROKER=ip_van_je_mqtt_broker
MQTT_USERNAME=mqtt_gebruikersnaam
MQTT_PASSWORD=mqtt_wachtwoord
SSH_PASSWORD=ssh_wachtwoord
```

3. Start de container:
```
docker-compose up -d
```









Tibber account with API token
MQTT broker
Home Assistant installation
🔧 Installation
Get your Tibber API token from developer.tibber.com
