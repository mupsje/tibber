# tibber
Docker to hassio


Ik wil graag de kale prijs in Hassio hebben om de zonnepanelen uit te schakelen wanneer de prijs in de min is.
Nu enkel alleen de prijs inclusief belasting.


![image](https://github.com/user-attachments/assets/cebf20b4-8faf-49dc-af22-5037e43794dc)


git clone deze ergens in je root.
pas de .env example aan naar de juiste waardes en rename naar .env

```
docker build -t tibber_mqtt .
```

dan 

```
docker run --env-file .env tibber_mqtt
```

In Hassio komt die in beeld.

Veel plezier
