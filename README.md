# Бот для подбора рецептов
## Запуск 
### Склонируйте репозиторий 
```commandline
git clone https://github.com/Artem09076/cookery_bookbot.git
``` 
### Настройте .env файл по примеру 

```
DB_HOST=db
DB_PORT=<your db host>
DB_NAME=<your db name>
DB_USER=<your db user>
DB_PASSWORD=<your db password>
BOT_TOKEN=<your token bot>
REDIS_HOST=redis
REDIS_PORT=<your redis port>
BOT_WEBHOOK_URL=<your webhook url> if exsist else ''
RABBIT_HOST= 'rabbitmq'
RABBIT_PORT = <your rabbit port>
RABBIT_USER = <your rabbit user>
RABBIT_PASSWORD = <your rabbit password>
```

### Запуск приложения
```commandline
docker compose up 
```




