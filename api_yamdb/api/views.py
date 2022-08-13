from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .confirmation import get_tokens_for_user, send_email
from .permissions import IsAdmin
from .serializers import (GettingTokenSerializer, OwnerSerializer, SignupSerializer,
                          UserSerializer)

User = get_user_model()


class SignupUserAPIView(generics.CreateAPIView):
    """Обработка запроса на регистрацию нового пользователя."""
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = get_object_or_404(
            User, username=serializer.validated_data['username']
        )
        confirmation_code = default_token_generator.make_token(user)
        send_email(serializer.validated_data['email'], confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenAuthApiView(generics.CreateAPIView):
    """Получение access-токена."""
    serializer_class = GettingTokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.validated_data['username']
        )
        if default_token_generator.check_token(
                user, serializer.validated_data['confirmation_code']):
            token = get_tokens_for_user(user)
            return JsonResponse({'token': token['access']},
                                status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Обработка запросов к эндпоинтам "users/", "users/username/"."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAdmin, )
    lookup_field = 'username'
    lookup_value_regex = '[^/]+'

    @action(methods=['get', 'patch'], detail=False,
            permission_classes=[IsAuthenticated, ],
            url_path='me', url_name='me')
    def performing_requests_to_me(self, request, pk=None):
        user = User.objects.get(username=request.user)
        if request.method == 'GET':
            serializer = OwnerSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = OwnerSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
