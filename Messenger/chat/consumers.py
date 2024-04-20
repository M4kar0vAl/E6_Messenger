import json

from zoneinfo import ZoneInfo
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.template.defaultfilters import date, time
from django.utils.timezone import localtime

from .models import Message, Chat


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.chat_pk = self.scope['url_route']['kwargs']['pk']
        self.chat_group_name = f'chat_{self.chat_pk}'

        async_to_sync(self.channel_layer.group_add)(
            self.chat_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_group_name, self.channel_name
        )
    
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        text = text_data_json['messageText']
        chat_pk = text_data_json['chatPk']
        chat = Chat.objects.get(pk=chat_pk)
        user = self.scope['user']

        tz_str = self.scope['cookies']['django_timezone']

        msg_obj = Message.objects.create(text=text, chat=chat, user=user)

        user_avatar_path = user.avatar.url if user.avatar else '/media/avatars/default/default.jpg'

        async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name, {
                'type': 'chat_message',
                'message_pk': msg_obj.pk,
                'username': user.username,
                'userAvatarPath': user_avatar_path,
                'tz_str': tz_str
            }
        )

    def chat_message(self, event):
        message_pk = event['message_pk']
        msg_obj = Message.objects.get(pk=message_pk)
        tz = ZoneInfo(event['tz_str'])
        local_created = localtime(msg_obj.created, tz)
        created_date = date(local_created, 'd-m-Y')
        created_time = time(local_created, 'G:i')
        username = event['username']
        user_avatar_path = event['userAvatarPath']

        self.send(text_data=json.dumps({
                'messageText': msg_obj.text,
                'messageTime': f'{created_date} {created_time}',
                'username': username,
                'userAvatarPath': user_avatar_path
        }))
