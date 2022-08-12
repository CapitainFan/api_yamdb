from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, SignupAdminAPIView, SignupUserAPIView,
                       TitleViewSet, UserViewAPI)
from django.urls import include, path
from rest_framework import routers

router_v1 = routers.DefaultRouter()
router_v1.register(r'genres', GenreViewSet, basename='Genre')
router_v1.register(r'categories', CategoryViewSet, basename='Category')
router_v1.register(r'titles', TitleViewSet, basename='Title')
router_v1.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', SignupUserAPIView.as_view()),
    path('v1/auth/signup/', SignupUserAPIView.as_view()),
    path('v1/users/', SignupAdminAPIView.as_view()),
    path('v1/users/<str:username>/', UserViewAPI.as_view()),
    path('v1/users/me/', UserViewAPI.as_view()),
]
