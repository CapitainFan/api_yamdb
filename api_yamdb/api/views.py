# from users.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .confirmation import get_tokens_for_user, send_email
from .permissions import IsAdmin
from .serializers import (CodeSerializer, SignupAdminSerializer,
                          SignupSerializer, UserSerializer,
                          TitleROSerializer, TitleRWSerializer,
                          ReviewSerializer, CommentSerializer,
                          CategorySerializer, GenreSerializer)
from reviews.models import Title, Category, Genre
from .permissions import IsOwnerOrIsAdmin
from .mixins import CreateDeleteListViewSet

User = get_user_model()


class UserViewAPI(APIView):
    pass


class SignupUserAPIView(generics.CreateAPIView):
    """Обработка запроса на регистрацию от нового пользователя"""
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
    serializer_class = CodeSerializer
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


class SignupAdminAPIView(generics.CreateAPIView,
                         generics.ListAPIView):
    """Обработка запроса к пользователям от админа"""
    serializer_class = SignupAdminSerializer
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    # permission_classes = (IsAdmin,) #IsAdmin


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
    permission_class = IsOwnerOrIsAdmin

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_class = IsOwnerOrIsAdmin

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
