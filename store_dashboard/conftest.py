"""
run tests with command: pytest --ignore=mongodata/ -vvl
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "store_dashboard.settings")

import django

django.setup()

import pymongo
import pytest
from dotenv import load_dotenv
from rest_framework.test import APIClient

from store_dashboard.asgi import application

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")


@pytest.fixture(scope="session")
def asgi_app():
    return application


@pytest.fixture(scope="session")
def test_client():
    test_client = APIClient()
    return test_client


@pytest.fixture(scope="session")
def mongodb():
    client = pymongo.MongoClient(f"mongodb://{DB_HOST}:27017")
    assert client.admin.command("ping").get("ok") == 1.0
    return client


@pytest.fixture(scope="session")
def fake_store(mongodb):
    db = mongodb.get_database(DB_NAME)
    s_collection = db.get_collection("Store")
    s_collection.insert_one({"store_id": "test123"})
    fake_store = s_collection.find_one({"store_id": "test123"})
    assert fake_store != None  # noqa
    try:
        yield fake_store
    finally:
        s_collection.delete_one({"store_id": "test123"})


@pytest.fixture
def fake_item(mongodb, fake_store):
    db = mongodb.get_database(DB_NAME)
    i_collection = db.get_collection("Item")
    i_collection.insert_one(
        {
            "store_id": fake_store.get("store_id"),
            "item_id": "Test_1",
            "quantity": 5,
        }
    )
    fake_item = i_collection.find_one({"item_id": "Test_1"})
    assert fake_item != None  # noqa
    try:
        yield fake_item
    finally:
        i_collection.delete_one({"item_id": "Test_1"})


@pytest.fixture
def fake_items(mongodb, fake_store):
    fake_items_list = [
        {"store_id": fake_store.get("store_id"), "item_id": "Test_2", "quantity": 10},
        {"store_id": fake_store.get("store_id"), "item_id": "Test_3", "quantity": 1},
    ]
    db = mongodb.get_database(DB_NAME)
    i_collection = db.get_collection("Item")
    res = i_collection.insert_many(fake_items_list)
    fake_items = [i_collection.find_one({"_id": i}) for i in res.inserted_ids]
    try:
        yield fake_items
    finally:
        for item in fake_items:
            i_collection.delete_one({"item_id": item.get("item_id")})
