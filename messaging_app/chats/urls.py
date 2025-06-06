from django.urls import path, include
from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter
from .views import CustomUserViewSet, MessageViewSet, ConversationViewSet

router = routers.DefaultRouter()
router.register(r'customusers', CustomUserViewSet, basename='customuser')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router for messages within a conversation
nested_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls))
]
