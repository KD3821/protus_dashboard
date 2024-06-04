# store_api

<h1  align="center">Simple Store API</h1>
<p align="center"><img src="https://img.shields.io/badge/made_by-KD3821-coral"></p><br>


<ul>

<li>Стек: Django(DRF), Django-Channels, Aiogram, Redis, Celery, Uvicorn, Pytest, Python 3.10+</li>

<li>Для MongoDB (версия 6+) используется образ без AVX - заменить при необходимости</li>

<li>Команда для запуска сервиса: CURRENT_UID=0:0 docker-compose -f docker-compose.yml up --build</li>

<li>Для проверки работы веб-сокетов можно использовать расширение "Web Socket Client" для браузера Google Chrome (адрес: ws://localhost:8000/ws/stores/{store_id})</li>

<li>Об .env файле:<br>STORE_IDS=abc111 xyz000 - id складов через пробел<br>SPECIAL_USER=ХХХХХХХХХ - телеграм ID получателя отчета<br>REPORT_TIME='18:25' - время ежедневного отчета (если не задано - отправляется в 21:00 по умолчанию)</li>

<li>Для прогона тестов запустить сервис с помощью команды: CURRENT_UID=0:0 docker-compose -f docker-compose.dev.yml up (в .env файле везде указать 127.0.0.1)</li> 

<li>Для отдельного запуска Django команда:<br>uvicorn store_dashboard.asgi:application.<br>Для отдельного запуска бота команда:<br>python3 report_bot.py.<br>Для отдельного запуска Celery команда:<br>python3 -m celery -A store_dashboard worker --beat --loglevel=info</li>

</ul>
