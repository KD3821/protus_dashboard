import json

from channels.generic.websocket import AsyncWebsocketConsumer


class StoreConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.store_id = self.scope.get('url_route').get('kwargs').get('store_id')
        await self.channel_layer.group_add(self.store_id, self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        type_data = data.get('type')
        report_data = data.get('report')
        await self.channel_layer.group_send(
            self.store_id,
            {
                'type': type_data,
                'report': report_data
             }
        )

    async def store_report(self, event):
        report_data = event.get('report')
        await self.send(text_data=json.dumps(report_data))
