# store_api

<h1  align="center">Simple Store API</h1>
<p align="center"><img src="https://img.shields.io/badge/made_by-KD3821-coral"></p><br>


<ul>

<li>Стек: Django(DRF), Django-Channels, Aiogram, Redis, Celery, Uvicorn, Pytest, Python 3.10+</li>

<li>Для MongoDB (версия 6+) используется образ без AVX - заменить при необходимости</li>

<li>Команда для запуска сервиса: CURRENT_UID=0:0 docker-compose -f docker-compose.yml up --build</li>

<li>Для проверки работы веб-сокетов можно использовать расширение "Web Socket Client" для браузера Google Chrome (адрес: ws://localhost:8000/ws/stores/{store_id})</li>

<li>Об .env файле:<br>STORE_IDS=abc111 xyz000 - id складов через пробел<br>SPECIAL_USER=ХХХХХХХХХ - телеграм ID получателя отчета<br>REPORT_TIME='18:25' - время ежедневного отчета (если не задано - отправляется в 21:00 по умолчанию)</li>

<li>Для прогона тестов запустить сервис с помощью команды:<br>CURRENT_UID=0:0 docker-compose -f docker-compose.dev.yml up<br>(в .env файле везде указать 127.0.0.1)</li> 

<li>Для отдельного запуска Django команда:<br>uvicorn store_dashboard.asgi:application.<br>Для отдельного запуска бота команда:<br>python3 report_bot.py.<br>Для отдельного запуска Celery команда:<br>python3 -m celery -A store_dashboard worker --beat --loglevel=info</li>

</ul>
<br>
<h3>Описание задания:</h3>
Представим, что у нас есть склад товаров. Нам нужно сделать API для управления остатками.

Даны: items и stores - модели на ваше усмотрение.

Используем:
- MongoDB
- FastApi / Django / Flask - без разницы
- Websockets
- docker-compose

**Все нужно покрыть тестами. И сокеты и API.**


Дополнительно:
1. Можно написать pod для kubernetes
2. Симулировать в тестах большую параллельную нагрузку на операции demand/supply, чтобы все корректно считалось
3. TG бот, отправляющий в 21 остатки склада


### GET /stores/{store_id}

#### RESPONSE

```
{
	store: {
		store_id: '',
		report: [{
			item_id: '',
			quantity: 10
		}]
	}
	
}
```


#### GET /stores/{store_id}/xlsx_report

#### RESPONSE

Должен отдавать файл с xlsx с текущими остатками склада. 

### POST /stores/{store_id}

#### REQUEST

```
{
	operation: 'demand', // supply
	item_id: '',
	quantity: 10
}
```

#### RESPONSE

```
{
	store: {
		store_id: '',
		report: []
	}
}
```



### POST /stores/{store_id}/group_op

#### REQUEST

```
{
	operation: 'demand', // supply
	items: [ {
		item_id: '',
		quantity: 10
	}]
}
```


#### RESPONSE

```
{
	store: {
		store_id: '',
		report: []
	}
}
```


### POST /stores/{store_id}/clean

#### RESPONSE

```
{
	store: {
		store_id: '',
		report: []
	}
}
```



### Websockets

Нужно обеспечить подключение к сообщением от склада по store_id.  В момент происхождения изменений должен отправляться report.

### TG-бот

Набросать телеграм бота, который будет отправлять в 21:00 отчет по остатку склада - только захардкоженному user_id.
