import os

import pymongo
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')

url = f'mongodb://{DB_HOST}:27017'

client = pymongo.MongoClient(url)

store_db = client[DB_NAME]


"""
run mongo in dev:
docker run --rm -ti -p 27017:27017 --name store_mongo nertworkweb/mongodb-no-avx --bind_ip_all
### or ####
CURRENT_UID=0:0 docker-compose up
"""