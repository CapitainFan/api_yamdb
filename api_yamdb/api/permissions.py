from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    message = 'Доступ разрешен только администратору.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_staff)
