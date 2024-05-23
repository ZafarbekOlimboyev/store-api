from rest_framework.permissions import BasePermission


class Cheak(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        elif request.method == 'DELETE':
            return request.user.is_superuser
        return request.user.is_staff or request.user.is_superuser


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return request.user.is_staff or request.user.is_superuser


class IsSuperUserOrAdminUser(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return request.user.is_staff
        return request.user.is_superuser
