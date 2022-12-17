from django.conf import settings
from django.db import models


class Room(models.Model):
    online = models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True, related_name='room')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='room_users_api')
    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    def __str__(self):
        return f'({self.get_online_count()})'


class Message(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='message')
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE, related_name='message')
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.timestamp}]'
