import json
from datetime import datetime
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone
from .models import Message

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
    
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope['user']

        # Save message to database
        m = Message.objects.create(content=message, user=user, room_id=self.room_name)

        # Convert created_date to local time and format it
        created_date_local = timezone.localtime(m.created_date)
        formatted_time = created_date_local.strftime("%H:%M")

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "chat_message", 
                "message": message,
                "user": user.username,
                "created_date": formatted_time
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        user = event['user']
        created_date = event['created_date']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            "message": message,
            "user": user,
            "created_date": created_date
        }))
