import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store_dashboard.settings')

import django
django.setup()

import pytest
import pymongo
from dotenv import load_dotenv
from rest_framework.test import APIClient


load_dotenv()


@pytest.fixture(scope="session")
def test_client():
    test_client = APIClient()
    return test_client


@pytest.fixture(scope="session")
def mongodb():
    client = pymongo.MongoClient(f"mongodb://{os.getenv('DB_HOST')}:27017")
    assert client.admin.command("ping").get("ok") == 1.0
    return client


@pytest.fixture
def rollback_session(mongodb):
    session = mongodb.start_session()
    session.start_transaction()
    try:
        yield session
    finally:
        session.abort_transaction()


@pytest.fixture(scope="session")
def fake_store(mongodb):
    db = mongodb.get_database(f"{os.getenv('DB_NAME')}")
    s_collection = db.get_collection('Store')
    s_collection.insert_one({"store_id": "test123"})
    fake_store = s_collection.find_one({"store_id": "test123"})
    assert fake_store != None  # noqa
    try:
        yield fake_store
    finally:
        s_collection.delete_one({"store_id": "test123"})
