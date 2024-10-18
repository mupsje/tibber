Dit is hetzelfde maar dan voor docker compose.

```
docker-compose build --no-cache
docker tag poepchen/my-tinytuya-app:latest poepchen/my-tinytuya-app:v1.1
docker push poepchen/my-tinytuya-app:v1.1
docker push poepchen/my-tinytuya-app:latest

docker-compose pull
docker-compose up -d
```

reminder
cd path/to/your_project

```
python -m venv env
```
- Windows
```
.\env\Scripts\activate
```
- macOS/Linux
```
 source env/bin/activate
```
When you're done working in the virtual environment, you can deactivate it by simply running:
```
deactivate
```

