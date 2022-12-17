from django.shortcuts import render

from chat.models import Room, Message


def index_view(request):
    return render(request, 'chat/index.html', {
        'rooms': Room.objects.all(),
    })


def room_view(request, id):
    chat_room, created = Room.objects.get_or_create(id=id)
    messages = Message.objects.filter(room=chat_room)
    return render(request, 'chat/room.html', {
        'room': chat_room,
        'messages': messages
    })
