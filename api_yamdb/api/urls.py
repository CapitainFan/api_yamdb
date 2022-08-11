from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from api.views import SignupAdminAPIView, SignupUserAPIView, UserViewAPI


urlpatterns = [
    path('v1/auth/token/', SignupUserAPIView.as_view()), # Add view here (POST)
    path('v1/auth/signup/', SignupUserAPIView.as_view()), # Add mail sending with conf code(POST)
    path('v1/users/', SignupAdminAPIView.as_view()), #  Add pagination here (GET/POST)
    # path('v1/users/<str:username>/', UserViewAPI.as_view()), #  Add view here (GET/PATCH/DELETE)
    # path('v1/users/me/', UserViewAPI.as_view()), #  Add view here (GET/PATCH)
]
