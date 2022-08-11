from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from api.views import SignupUserAPIView, SignupAdminAPIView, TokenAuthApiView


urlpatterns = [
    path('v1/auth/token/', TokenAuthApiView.as_view()),
    path('v1/auth/signup/', SignupUserAPIView.as_view()),
    path('v1/users/', SignupAdminAPIView.as_view()), # username и me через utl_path
    # path('v1/users/<str:username>/', UserViewAPI.as_view()), #  Add view here (GET/PATCH/DELETE)
    # path('v1/users/me/', UserViewAPI.as_view()), #  Add view here (GET/PATCH)
]
