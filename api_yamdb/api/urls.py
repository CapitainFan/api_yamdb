from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (CommentViewSet, ReviewViewSet)

routerv2 = DefaultRouter()
routerv2.register('review', ReviewViewSet, basename='reviws')
routerv2.register('comment', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(routerv2.urls)),
]
