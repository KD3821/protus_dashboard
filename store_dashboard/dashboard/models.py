import os

from dotenv import load_dotenv

from db_connection import store_db

load_dotenv()

STORE_IDS = os.getenv("STORE_IDS").split(" ")

stores_collection = store_db["Store"]

items_collection = store_db["Item"]

for i in STORE_IDS:
    store = {"store_id": i}
    s = stores_collection.find_one(store)
    if s is None:
        stores_collection.insert_one(store)
