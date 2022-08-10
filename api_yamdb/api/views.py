from .serializers import CategorySerializer, GenreSerializer, TitleROSerializer, TitleRWSerializer
from .mixins import CreateDeleteListViewSet
from reviews.models import Category, Genre, Title
from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend


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
