from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.permissions import BasePermission

User = get_user_model()


class IsAdmin(BasePermission):
    allowed_user_roles = ('admin', )

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role in self.allowed_user_roles:
                return True
        return False


class IsModerator(BasePermission):
    allowed_user_roles = ('moderator', )

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role in self.allowed_user_roles:
                return True
        return False


class IsUser(BasePermission):
    allowed_user_roles = ('user', )

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role in self.allowed_user_roles:
                return True
        return False


# Мои правки, класс для сэйф методов без auth

class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_staff
