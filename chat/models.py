from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.response import Response

User = get_user_model()


class Contact(models.Model):
    user = models.ForeignKey(
        User, related_name='friends', on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user
        # if self.user.pictures == "":
        #     return '{user_id: ' + str(self.user.id) + \
        #            ', first_name: ' + self.user.first_name + \
        #            ', last_name: ' + self.user.last_name + \
        #            ', pictures: null' + '}'
        #
        # return '{user_id: ' + str(self.user.id) + \
        #        ', first_name: ' + self.user.first_name + \
        #        ', last_name: ' + self.user.last_name + \
        #        ', pictures: ' + str(self.user.pictures) + '}'

    def __repr__(self):
        return Response(
            {
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'user_id': self.user.id,
                "pictures": self.user.pictures
            }
        )


class Message(models.Model):
    contact = models.ForeignKey(
        Contact, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact.user.email


class Chat(models.Model):
    participants = models.ManyToManyField(
        Contact, related_name='chats', blank=True)
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return "{}".format(self.pk)
