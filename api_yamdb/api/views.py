from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import (SignupAdminSerializer, SignupSerializer,
                             UserSerializer)

# from users.models import User
from .confirmation import code_generation, send_email

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
        if not User.objects.filter(username=request.data['username'], email=request.data['email']).exists():
            if serializer.is_valid():
                serializer.save()
                send_email(request.data['username'])
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        send_email(request.data['email'])
        return Response(status=status.HTTP_200_OK)


class SignupAdminAPIView(generics.CreateAPIView,
                         generics.ListAPIView):
    """Обработка запроса создание нового пользователя от админа"""
    serializer_class = SignupAdminSerializer
    queryset = User.objects.all()
    # permission_classes = (AllowAny,) ADMIN
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

