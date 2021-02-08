# QUIZ BOT (VK, Telegram)
Бот для проведение викторин в VK и Telegram). С помощью этих ботов Вы, можете проводить викторины (вопрос\ответ). 

Для хранение данных бота используется .

### Для запуска бота вам необходимо:
* Python 3  
* Redis

## Установка
Установите зависимости
```
pip3 install -r requirements.txt
```

Установите переменные окружения
```
TELEGRAM_BOT_TOKEN=токен бота в телеграмме (если хотите запускать бота для telegram)
VK_API_KEY=токен бота в vk (если хотите запускать бота для ВК)

REDIS_HOST=хост redis
REDIS_PASSWORD=пароль redis
REDIS_PORT=порт redis
```

## Запуск бота  

Для запуска в VK
```
python3 bot_vk.py
```

Для запуска бота в Telegram
```
python3 bot-tg.py
```
