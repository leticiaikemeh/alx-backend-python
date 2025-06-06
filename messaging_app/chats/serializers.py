from rest_framework import serializers
from .models import CustomUser, Conversation, Message
from django.contrib.auth.hashers import make_password


class CustomUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={"input_type": "password"}
    )
    class Meta:
        model = CustomUser
        fields = [
            'user_id', 'email', 'username', 'first_name',
            'last_name', 'phone_number', 'created_at'
        ]
    
    def create(self, validated_data):
        # Hash the password
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())
    conversation = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all()
    )

    class Meta:
        model = Message
        fields = [
            'message_id', 'sender', 'conversation',
            'message_body', 'sent_at'
        ]


class ConversationSerializer(serializers.ModelSerializer):
    participants = CustomUserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    total_messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants',
            'messages', 'total_messages', 'created_at'
        ]

    def get_total_messages(self, obj):
        return obj.messages.count()
