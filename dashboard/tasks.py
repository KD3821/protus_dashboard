import os

import requests
from celery import shared_task
from dotenv import load_dotenv

from .models import stores_collection
from .utils import StoreProcessor

load_dotenv()


@shared_task
def send_bot_report():
    store_total = "ПОЛНЫЙ ОТЧЕТ:\n"
    cursor = stores_collection.find({})
    for store in cursor:
        sp = StoreProcessor(store.get('store_id'))
        items = sp.get_items()
        store_total += f"*****\nstore_id: {store.get('store_id')}\n*****\n"
        for item in items:
            store_total += f"item_id: {item.get('item_id')}\nquantity: {item.get('quantity')}\n-----\n"
    requests.post(
        f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/sendMessage",
        data={
            "chat_id": os.getenv("SPECIAL_USER"),
            "text": store_total
        }
    )
