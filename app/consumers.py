import json
from channels.generic.websocket import AsyncWebsocketConsumer
# your_app_name/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User

class SingleChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope["user"].id
        self.user = self.scope["user"]
        
        self.other_user_id = self.scope['url_route']['kwargs']['other_user_id']
        self.other_user = await sync_to_async(User.objects.get)(id=self.other_user_id)
        
        self.room_name = f'{min(self.user_id, self.other_user_id)}_{max(self.user_id, self.other_user_id)}'
        self.room_group_name = f'chat_{self.room_name}'

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

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        await sync_to_async(ChatMessage.objects.create)(
            message_by=self.user,
            receive_by=self.other_user,
            message=message
        )
       
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'message_by': self.user_id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        msg_by = event['message_by']
        
        await self.send(text_data=json.dumps({
            'message': message,
            'msg_by': msg_by,
        }))


# --------------------------- Group chat logic 



# your_app_name/consumers.py
class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        self.room_group_name = f'chat_{self.group_name}'

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

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
