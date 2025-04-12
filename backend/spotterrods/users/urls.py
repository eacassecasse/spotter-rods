from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

from .views import UserCreate
from .views import UserLogin
from .views import Logout
from .views import UserDetail
from .views import TokenRefresh
from .views import PasswordSetupView

urlpatterns = [
    path('refresh/', TokenRefresh.as_view(), name='refresh-token'),
    path('register/', UserCreate.as_view(), name='user-registration'),
    path('login/', UserLogin.as_view(), name='user-authentication'),
    path('logout/', Logout.as_view(), name='user-logout'),
    path('setup-password/', PasswordSetupView.as_view(), name='setup-password'),
    path('profile/', UserDetail.as_view(), name='user-details'),
]
