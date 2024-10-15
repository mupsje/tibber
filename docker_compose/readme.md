Dit is hetzelfde maar dan voor docker compose.

```
docker-compose build
docker tag poepchen/my-tinytuya-app:latest poepchen/my-tinytuya-app:v1.1
docker push poepchen/my-tinytuya-app:v1.1
docker push poepchen/my-tinytuya-app:latest

docker-compose pull
docker-compose up -d
```




