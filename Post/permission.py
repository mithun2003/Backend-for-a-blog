from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, and OPTIONS requests for all users
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Check if the request user is the creator of the object
        return obj.user_id == request.user.id
