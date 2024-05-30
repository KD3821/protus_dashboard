import json

from channels.generic.websocket import AsyncWebsocketConsumer


class StoreConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.store_id = self.scope.get('url_route').get('kwargs').get('store_id')
        await self.accept()

    async def receive(self, text_data):
        pass