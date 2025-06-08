#!/usr/bin/python3

"""

"""

from rest_framework import serializers
from .models import User, Message, Conversation


class UserSerializer(serializers.ModelSerializer):
    """ serialize the User class """

    class Meta:
        model = User
        fields = (
                'user_id',
                'first_name',
                'last_name',
                'phone_number',
            )



class MessageSerializer(serializers.ModelSerializer):
    """ serialize the Message class """

    sender = UserSerializer()

    class Meta:
        model = Message
        fields = (
                'message_id',
                'sender',
                'message_body',
                'sent_at',
                'created_at'
            )

    def validate_message_body(self, value):
        if len(self.value) == 0:
            raise serializers.ValidationError(
                    'You cannot send an empty message'
                    )
        return value


class ConversationSerializer(serializers.ModelSerializer):
    """ serialize the Conversation class """
    
    messages = MessageSerializer(many=True, read_only=True)
    total_messages = serializers.SerializerMethodField()

    def get_total_messages(self, obj):
        return obj.messages.count()


    class Meta:
        model = Conversation
        fields = (
                'conversation_id',
                'created_at',
                'messages',
                'total_messages',
            )
