from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .permissions import IsParticipantOfConversation
from rest_framework import viewsets, status, filters
from .models import CustomUser, Message, Conversation
from .filters import MessageFilter
from .pagination import MessagePagination
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import MessageSerializer, ConversationSerializer

@api_view(['GET'])
def home(request):
    """ """
    return HttpResponse('<h1>Home Page</h1>')

class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    serializer_class = MessageSerializer
    filterset_class = MessageFilter
    pagination_class = MessagePagination

    def get_queryset(self):
        return Message.objects.filter(conversation__particpants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validate_data.get('conversation')
        conversation_id = conversation.id
        if self.request.user not in conversation__participants.all():
            return Response({'message': 'You can not send a message to this conversation'}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(sender=self.request.user)

    def perform_update(self, serializer):
        conversation = serializer.instance.conversation
        if self.request.user not in conversation__participants.all():
            raise PermissionDenied('You are not a participant in this conversation')
        serializer.save()

class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)
    
