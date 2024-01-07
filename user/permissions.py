from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff and request.user.is_admin)

class IsModUser(BasePermission):
    """
    Allows access only to mod users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
