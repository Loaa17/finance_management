import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'user_{self.user_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def notification(self, event):
        message_data = {
            'type': 'notification',
            'message': event.get('message', ''),
            'bonus_id': event.get('bonus_id', None),  # Changed from bonus_request_id to bonus_id
            'notification_type': event.get('notification_type', 'DEFAULT'),
        }
        await self.send(text_data=json.dumps(message_data))