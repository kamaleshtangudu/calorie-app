from rest_framework.permissions import BasePermission

from apps.users import constants as user_constants


class IsAdmin(BasePermission):
    """
    Allows access only to Active User.
    """

    def has_permission(self, request, view):
        return request.user.role == user_constants.UserRoles.ADMIN
