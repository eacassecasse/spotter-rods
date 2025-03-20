from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from .views import UserCreate
from .views import UserLogin
from .views import UserDetail

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token-obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('register/', UserCreate.as_view(), name='user-registration'),
    path('login/', UserLogin.as_view(), name='user-authentication'),
    path('profile/', UserDetail.as_view(), name='user-details'),
]
