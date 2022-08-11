from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    message = 'Доступ разрешен только администратору.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated and (
                request.user.role == 'admin' or request.user.is_staff)
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated and (
                request.user.role == 'admin' or request.user.is_staff)
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_staff)

# class IsUser(permissions.BasePermission):
#     message = ('Изменение данных доступно только'
#                'владельцу аккаунта.')

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return obj.user == request.user
#         return obj.user == request.user


# class IsOwnerOrIsAdmin(permissions.BasePermission):
#     message = ('Изменение данных доступно только'
#                'автору, модератору или администаратору!')

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return (obj.user == request.user
#                 or request.user.is_stuff
#                 or request.user.admin
#                 or request.user.moderator)

