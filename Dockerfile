# Gebruik een Alpine-image met Python 3.12.5
FROM python:3.12.5-alpine

# Zet de werkdirectory in de container
WORKDIR /app

# Installeer de benodigde systeembibliotheken
RUN apk add --no-cache gcc musl-dev libffi-dev

# Kopieer de requirements.txt naar de container
COPY requirements.txt .

# Installeer de Python-afhankelijkheden
RUN pip install --no-cache-dir -r requirements.txt

# Kopieer de applicatiebestanden naar de container
COPY . .

# Stel het commando in om het script uit te voeren
CMD ["python", "tibber_energy_monitor.py"]
