from django.db import models
from django.db.models import CharField, IntegerField, ForeignKey

from db_connection import store_db


class Store(models.Model):
    store_id = CharField(max_length=10)
    name = CharField(max_length=20)

    class Meta:
        abstract = True


class Item(models.Model):
    item_id = CharField(max_length=10)
    name = CharField(max_length=20)
    quantity = IntegerField(default=0)
    store = ForeignKey(Store, on_delete=models.CASCADE, related_name='items')

    class Meta:
        abstract = True


stores_collection = store_db['Store']

items_collection = store_db['Item']

store_ids = ['abc111', 'xyz000']

for i in store_ids:
    store = {'store_id': i}
    s = stores_collection.find(store)
    if not s.retrieved:
        stores_collection.insert_one(store)
