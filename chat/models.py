from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class ChatRoom(models.Model):
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Chat {self.id} - {", ".join([user.username for user in self.participants.all()])}'

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.sender.username}: {self.content[:50]}'

    class Meta:
        ordering = ['timestamp']
