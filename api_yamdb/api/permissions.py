from rest_framework.permissions import SAFE_METHODS, BasePermission


class AuthorAndOthersOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or self.role == "user"
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or (
                self.role == "user" and (
                    (obj.author == request.user)
                    or (self.role == "admin")
                )
            )
        )
