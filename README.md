<div align="left">
    <img src="assets\tibber-vector-logo.png" width="40%" align="left" style="margin-right: 15px"/>
    <div style="display: inline-block;">
        <h2 style="display: inline-block; vertical-align: middle; margin-top: 0;">TIBBER</h2>
        <p>
	<em><code>Applicatie haalt real-time energieprijzen op van Tibber en publiceert ze naar Home Assistant via MQTT.</code></em>
</p>
        <p>
	<img src="https://img.shields.io/github/license/mupsje/tibber?style=flat-square&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/mupsje/tibber?style=flat-square&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/mupsje/tibber?style=flat-square&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/mupsje/tibber?style=flat-square&color=0080ff" alt="repo-language-count">
</p>
        <p>Built with the tools and technologies:</p>
        <p>
	<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=flat-square&logo=Docker&logoColor=white" alt="Docker">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat-square&logo=Python&logoColor=white" alt="Python">
</p>
    </div>
</div>
<br clear="left"/>

<div align="center">
# Tibber Energy Monitor

![image](https://github.com/user-attachments/assets/cebf20b4-8faf-49dc-af22-5037e43794dc)
</div>


## 🔗 Quick Links

- [📍 Overview](#-overview)
- [👾 Features](#-features)
- [📁 Project Structure](#-project-structure)
  - [📂 Project Index](#-project-index)
- [🚀 Getting Started](#-getting-started)
  - [☑️ Prerequisites](#-prerequisites)
  - [⚙️ Installation](#-installation)
  - [🤖 Usage](#🤖-usage)
  - [🧪 Testing](#🧪-testing)
- [📌 Project Roadmap](#-project-roadmap)
- [🔰 Contributing](#-contributing)
- [🎗 License](#-license)
- [🙌 Acknowledgments](#-acknowledgments)

---

Deze applicatie haalt real-time energieprijzen op van Tibber en publiceert ze naar Home Assistant via MQTT.
Ik wil graag de kale prijs in Hassio hebben om de zonnepanelen uit te schakelen wanneer de prijs in de min is. (negatief)
Nu zien wij enkel alleen de prijs inclusief belasting, en daar hebben we niks aan.

## ✨Functionaliteiten
- Real-time energieprijzen van Tibber
- Automatische integratie met Home Assistant via MQTT discovery
- Prijsupdates elke 5 minuten
- SSH toegang voor beheer
- Draait in Docker container

## 📋Vereisten
- Docker en Docker Compose
- Tibber account en API token
- MQTT broker (bijvoorbeeld Mosquitto)
- Home Assistant

## 🚀Installatie

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

## Configuratie🔧

Tibber Token 🔑 
  - Log in op developer.tibber.com
  - Genereer een nieuwe access token
  - Plaats deze in het .env bestand

MQTT 📡
  - Zorg dat je MQTT broker draait
  - Vul de juiste MQTT gegevens in het .env bestand in
  - De applicatie maakt automatisch de entities aan in Home Assistant

SSH Toegang 🔐
  - SSH toegang is mogelijk op poort 22
  - Gebruik root als gebruikersnaam
  - Wachtwoord is ingesteld via SSH_PASSWORD in .env

Sensors in Home Assistant
De volgende sensors worden automatisch aangemaakt:
  - 💰 Tibber Energie Prijs (EUR/kWh)
  - 📈 Tibber Belasting Prijs (EUR/kWh)
  - 💶 Tibber Totaal Prijs (EUR/kWh)

Onderhoud 🛠️
  - Logs bekijken: docker-compose logs -f
  - Container herstarten: docker-compose restart
  - SSH verbinding: ssh root@[container-ip]
    
Netwerk 🌐
  - Container heeft een vast IP nodig
  - Configureer het netwerk in docker-compose.yml
  - Zorg dat de container toegang heeft tot internet en je MQTT broker

Support 📫
Bij vragen of problemen, open een issue in de GitHub repository.


