import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from users.models import User
from .models import Room, Message
from rest_framework_simplejwt.tokens import AccessToken


class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None
        self.user_inbox = None
        self.token = None

    def connect(self):
        if self.scope.get('query_string', None):
            token = self.scope.get('query_string').decode('utf-8')[6:]
            if token:
                user_id = AccessToken(token).get('user_id', None)
                self.user = User.objects.get(id=user_id)
        else:
            self.user = self.scope['user']

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name
        self.room = Room.objects.get(id=self.room_name)
        self.user_inbox = f'inbox_{self.user.username}'
        print(self.user)
        # connection has to be accepted
        self.accept()

        # join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

        # send the user list to the newly joined user
        self.send(json.dumps({
            'type': 'user_list',
            'users': [user.id for user in self.room.online.all()],
            'is_online': True if self.room.online.exclude(username=self.user.username) else False
        }))

        if self.user.is_authenticated:
            # create a user inbox for private messages
            async_to_sync(self.channel_layer.group_add)(
                self.user_inbox,
                self.channel_name,
            )

            # send the join event to the room
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'user_join',
                    'user': self.user.id,
                }
            )
            self.room.online.add(self.user)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

        if self.user.is_authenticated:
            # delete the user inbox for private messages
            async_to_sync(self.channel_layer.group_add)(
                self.user_inbox,
                self.channel_name,
            )

            # send the leave event to the room
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'user_leave',
                    'user': self.user.id,
                }
            )
            self.room.online.remove(self.user)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if not self.user.is_authenticated:
            return
        if message.startswith('/pm '):
            split = message.split(' ', 2)
            target = split[1]
            target_msg = split[2]

            # send private message to the target
            async_to_sync(self.channel_layer.group_send)(
                f'inbox_{target}',
                {
                    'type': 'private_message',
                    'user': self.user.id,
                    'message': target_msg,
                }
            )
            # send private message delivered to the user
            self.send(json.dumps({
                'type': 'private_message_delivered',
                'target': target,
                'message': target_msg,
            }))
            return

        # send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user': self.user.id,
                'message': message,

            }
        )
        Message.objects.create(user=self.user, room=self.room, content=message)

    def chat_message(self, event):
        print(json.dumps(event))
        self.send(text_data=json.dumps(event))

    def user_join(self, event):
        self.send(text_data=json.dumps(event))

    def user_leave(self, event):
        self.send(text_data=json.dumps(event))

    def private_message(self, event):
        self.send(text_data=json.dumps(event))

    def private_message_delivered(self, event):
        self.send(text_data=json.dumps(event))
