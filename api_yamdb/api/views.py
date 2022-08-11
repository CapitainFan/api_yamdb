# from users.models import User
from django.contrib.auth import get_user_model
# from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters, generics, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.confirmation import (code_create_or_update, code_generation,
                              get_tokens_for_user, send_email)
from api.permissions import IsAdmin, IsUser
from api.serializers import (CodeSerializer, SignupAdminSerializer,
                             SignupSerializer, UserSerializer)
from reviews.models import Category, Genre, Title

from .mixins import CreateDeleteListViewSet
from .permissions import AuthorAndOthersOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleROSerializer,
                          TitleRWSerializer)

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

class CategoryViewSet(CreateDeleteListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )


class GenreViewSet(CreateDeleteListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.select_related(
        'category').prefetch_related('genre').all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleROSerializer
        return TitleRWSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_class = AuthorAndOthersOrReadOnly

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_class = AuthorAndOthersOrReadOnly

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        try:
            review = title.reviews.get(id=self.kwargs.get('review_id'))
        except TypeError:
            TypeError('У произведения нет такого отзыва')
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        try:
            review = title.reviews.get(id=self.kwargs.get('review_id'))
        except TypeError:
            TypeError('У произведения нет такого отзыва')
        serializer.save(author=self.request.user, review=review)

