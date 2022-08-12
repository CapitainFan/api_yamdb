from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    message = 'Доступ разрешен только администратору.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.admin or request.user.is_stuff
        return request.user.admin or request.user.is_stuff


class IsUser(permissions.BasePermission):
    message = ('Изменение данных доступно только'
               'владельцу аккаунта.')

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.user == request.user
        return obj.user == request.user


class IsOwnerOrIsAdmin(permissions.BasePermission):
    message = ('Изменение данных доступно только'
               'автору, модератору или администаратору!')

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.user == request.user
                or request.user.is_stuff
                or request.user.admin
                or request.user.moderator)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение на уровне админ."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_admin
            )
        )


class AuthorAndStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    obj.author == request.user
                    or request.user.is_moderator
                )
            )
        )


class OwnerOrAdmins(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_admin
                or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj == request.user
            or request.user.is_admin
            or request.user.is_superuser)
