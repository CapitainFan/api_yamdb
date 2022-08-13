from django.urls import include, path
from rest_framework import routers

from api.views import SignupUserAPIView, TokenAuthApiView, UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path(r'v1/auth/token/', TokenAuthApiView.as_view()),
    path(r'v1/auth/signup/', SignupUserAPIView.as_view()),
    path('v1/', include(router_v1.urls)),
]
