from django.urls import include, path
from rest_framework import routers
from api.views import GenreViewSet, CategoryViewSet, TitleViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'genres', GenreViewSet, basename='Genre')
router_v1.register(r'categories', CategoryViewSet, basename='Category')
router_v1.register(r'titles', TitleViewSet, basename='Title')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]