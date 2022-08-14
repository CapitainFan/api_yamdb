from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet,
                    ReviewViewSet, GenreViewSet,
                    SignupUserAPIView, TokenAuthApiView,
                    TitleViewSet, UserViewSet, )

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', TokenAuthApiView.as_view()),
    path('auth/signup/', SignupUserAPIView.as_view()),
]
