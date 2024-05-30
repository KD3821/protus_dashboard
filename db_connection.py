import pymongo

url = 'mongodb://localhost:27017'

client = pymongo.MongoClient(url)

store_db = client['MyStore']


"""
command for docker:
docker run --rm -ti -p 27017:27017 --name store_mongo nertworkweb/mongodb-no-avx --bind_ip_all
###
command for docker-compose:
CURRENT_UID=0:0 docker-compose up
"""