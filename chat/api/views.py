from rest_framework import viewsets

from .serializers import MessageSerializer, RoomSerializer, RoomPostSerializer
from ..models import Message, Room


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return RoomPostSerializer
        else:
            return self.serializer_class
