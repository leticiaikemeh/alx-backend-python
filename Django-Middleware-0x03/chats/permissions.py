from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    allow participants of a conversation to read, write and delete conversation(s)
    """
    def has_permissions(self, request, view):
        """
        checks if user is aunthenticated
        """
        return request.user and request.user.is_authenticated


    def has_object_permission(self, request, view, obj):
        """
        checks if user has permission to interact with Conversation Object
        """
        if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user in obj.participants.objects.all()
        return False
