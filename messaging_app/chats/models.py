from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone

class CustomUser(AbstractUser):
    """
    Custom user model using email for login.
    """
    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
        )
    email = models.EmailField(
        unique=True,
        max_length=255
        )
    username = models.CharField(
        max_length=100,
        unique=True
        )
    first_name = models.CharField(
        max_length=100,
        blank=False,
        null=False
        )
    last_name = models.CharField(
        max_length=100,
        blank=False,
        null=False)
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
        )
    password = models.CharField(
        max_length=128,
        blank=False,
        null=False
        )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user_id} {self.email})"


class Conversation(models.Model):
    conversation_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        primary_key=True)
    participants = models.ManyToManyField(
        'CustomUser',
        related_name='conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation ({self.conversation_id})"

class Message(models.Model):
    message_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        primary_key=True
    )
    sender = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message ({self.sender.username} - {self.content[:30]})"