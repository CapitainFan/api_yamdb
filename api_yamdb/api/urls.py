from django.urls import include, path
from rest_framework import routers
from api.views import GenreViewSet, CategoryViewSet, TitleViewSet

router = routers.DefaultRouter()
router.register(r'genres', GenreViewSet, basename='Genre')
router.register(r'categories', CategoryViewSet, basename='Category')
router.register(r'titles', TitleViewSet, basename='Title')

urlpatterns = [
    path('v1/', include(router.urls)),
]