from rest_framework import serializers

from chat.models import Message, Room
from products.serializers import UserProductSerializer


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    users = UserProductSerializer(read_only=True, many=True)

    class Meta:
        model = Room
        fields = '__all__'


class RoomPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        exclude = ['online']
