from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class AuthorAndOthersOrReadOnly(BasePermission):
    pass
