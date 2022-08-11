from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
# from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
# from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from django.http import JsonResponse

from api.serializers import SignupSerializer, UserSerializer, SignupAdminSerializer, CodeSerializer
# from users.models import User
from api.confirmation import send_email, code_generation, code_create_or_update, get_tokens_for_user
from api.permissions import IsAdmin, IsUser

from django.contrib.auth import get_user_model

User = get_user_model()



class UserViewAPI(APIView):
    pass
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (AllowAny,)

#     def get(self, request, *args, **kwargs):
#         user = User.objects.all()
#         serializer = UserSerializer(user, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


class SignupUserAPIView(generics.CreateAPIView):
    """Обработка запроса на регистрацию от нового пользователя"""
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not User.objects.filter(
            username=request.data['username'],
            email=request.data['email']
        ).exists():
            if serializer.is_valid():
                serializer.save()
                code_create_or_update(serializer.data['username'], serializer.data['email'])
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        code_create_or_update(request.data['username'], request.data['email'])
        return JsonResponse({'username': request.data['username'], 'email': request.data['email']}, status=status.HTTP_200_OK)


class TokenAuthApiView(generics.CreateAPIView):
    """Получение access-токена."""
    serializer_class = CodeSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User,
                username=serializer.data['username'],
                confirmation_code=serializer.data['confirmation_code'])
            token = get_tokens_for_user(user)
            return JsonResponse({'token': token['access']}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupAdminAPIView(generics.CreateAPIView,
                         generics.ListAPIView):
    """Обработка запроса к пользователям от админа"""
    serializer_class = SignupAdminSerializer
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAdmin,) #IsAdmin


# Переписать user на вьюсет
# class UserViewSet(viewsets.ModelViewSet):
#     serializer_class = SignupAdminSerializer
