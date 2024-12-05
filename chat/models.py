from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class ChatRoom(models.Model):
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    created_at = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=255, blank=True)
    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or f'Chat {self.id} - {", ".join([user.username for user in self.participants.all()])}'

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to='chat_files/', null=True, blank=True)
    read_by = models.ManyToManyField(User, related_name='read_messages', blank=True)
    
    def __str__(self):
        return f'{self.sender.username}: {self.content[:50]}'

    class Meta:
        ordering = ['timestamp']

class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(default=timezone.now)
    is_typing = models.ForeignKey(ChatRoom, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {"Online" if self.is_online else "Offline"}'
