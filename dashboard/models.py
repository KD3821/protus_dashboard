from db_connection import store_db


stores_collection = store_db['Store']

items_collection = store_db['Item']

ws_collection = store_db['WebSocket']

store_ids = ['abc111', 'xyz000']

for i in store_ids:
    store = {'store_id': i}
    s = stores_collection.find_one(store)
    if s is None:
        stores_collection.insert_one(store)
