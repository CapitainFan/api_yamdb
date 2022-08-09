from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet, ReviewViewSet

router = DefaultRouter()
router.register('follow', ReviewViewSet, basename='reviws')
router.register('coment', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
