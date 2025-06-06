from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, MessageViewSet, ConversationViewSet

router = DefaultRouter()
router.register(r'customusers', CustomUserViewSet, basename='customuser')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'conversations', ConversationViewSet, basename='conversation')

urlpatterns = [
    path('', include(router.urls)),
]
