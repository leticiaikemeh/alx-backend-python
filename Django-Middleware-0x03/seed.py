import os
import django
import uuid
import random
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging_app.settings')  # Adjust if your settings file path is different
django.setup()

from chats.models import User, Conversation, Message

def create_users(n=5):
    users = []
    for i in range(n):
        user = User.objects.create_user(
            username=f"user{i}",
            email=f"user{i}@example.com",
            password="password123",
            first_name=f"First{i}",
            last_name=f"Last{i}",
            phone_number=f"080000000{i}"
        )
        users.append(user)
    return users

def create_conversations(users, n=5):
    conversations = []
    for i in range(n):
        conv = Conversation.objects.create()
        participants = random.sample(users, 2)
        conv.participants.set(participants)
        conversations.append(conv)
    return conversations

def create_messages(users, conversations, n=10):
    for _ in range(n):
        conv = random.choice(conversations)
        sender = random.choice(list(conv.participants.all()))
        Message.objects.create(
            sender=sender,
            conversation=conv,
            message_body=f"This is a test message from {sender.username}",
            sent_at=datetime.now(),
            created_at=datetime.now() - timedelta(minutes=random.randint(1, 1000))
        )

if __name__ == "__main__":
    users = create_users()
    convs = create_conversations(users)
    create_messages(users, convs)
    print("✅ Seed data created.")

