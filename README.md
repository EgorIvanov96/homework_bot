# Homework_bot

## Homework_bot - это телеграм бот для предназначен для проверки статуса отправленной работы на ревью кода.


## Технологии

Проект "Homework_bot" использует следующие технологии:


- Python
- Python-telegram-bot
- Pytest


## Установка  

### Клонировать репозиторий и перейти в него в командной строке:

```bash
git@github.com:EgorIvanov96/homework_bot.git
```

```bash
cd homework_bot
```

### Создать и активировать виртуальное окружение:

```bash
python -m venv env
```

```bash
source env/bin/activate
```

### Установить в зависимости:

```bash
python -m pip install --upgrade pip
```

```bash
requirements.txt
```


### Записать в переменные окружения (файл .env) необходимые ключи:

- профиль токенов на Яндекс.Практикуме
- токен телеграм-бота
- свой ID в телеграме

## Пример: 

```bash
PRACTICUM_TOKEN=y0_AgAAAABKL-lcAAYckQAAAADlZOowY6dcsnfriIFEFEEFWFN218RE32ND

TELEGRAM_TOKEN=15430044356:AAF3WNIsYF_oE_fERRTEREJNGT GTG4

TELEGRAM_CHAT_ID=8888777333
```

## Запустить проект:

```bash
python homework.py
```
