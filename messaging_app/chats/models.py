from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import uuid

# Create your models here.

class User(AbstractUser):
    """ """
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, blank=False, null=False, unique=True)
    password = models.CharField(max_length=128, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return '{} {} - {}'.format(self.first_name, self.last_name, self.email)


class Conversation(models.Model):
    """ """
    conversation_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Conversation ({})'.format(self.conversation_id)


class Message(models.Model):
    """ """
    message_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Message ({} - {})'.format(self.sender.first_name, self.message_body[:30])
