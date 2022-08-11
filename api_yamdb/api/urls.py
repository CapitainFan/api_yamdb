from django.urls import include, path
from rest_framework import routers
from api.views import GenreViewSet, CategoryViewSet, TitleViewSet, SignupAdminAPIView, SignupUserAPIView, UserViewAPI, CommentViewSet, ReviewViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'genres', GenreViewSet, basename='Genre')
router_v1.register(r'categories', CategoryViewSet, basename='Category')
router_v1.register(r'titles', TitleViewSet, basename='Title')
router_v1.register(r'review', ReviewViewSet, basename='reviws')
router_v1.register(r'comment', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', SignupUserAPIView.as_view()), # Add view here (POST)
    path('v1/auth/signup/', SignupUserAPIView.as_view()), # Add mail sending with conf code(POST)
    path('v1/users/', SignupAdminAPIView.as_view()), #  Add pagination here (GET/POST)
    # path('v1/users/<str:username>/', UserViewAPI.as_view()), #  Add view here (GET/PATCH/DELETE)
    # path('v1/users/me/', UserViewAPI.as_view()), #  Add view here (GET/PATCH)
]
