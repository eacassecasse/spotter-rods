#!/usr/bin/python3
""" User View Module for SpotterRODS project """

import datetime
from django.core.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from django.core.cache import cache
from django.http import Http404

from core.models import BaseModel
from ..models import User, UserRoles
from ..serializers import UserSerializer, UserLoginSerializer
from spotterrods import ENV


def _set_cookie(response, key, value, path, max_age):
    response.set_cookie(
            key=key,
            value=value,
            httponly=True,
            secure=True,
            samesite=ENV.get('AUTH_COOKIE_SAMESITE', None),
            domain=ENV.get('AUTH_COOKIE_DOMAIN', None),
            path=path,
            max_age=max_age
        )
    
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id

class IsTechnician(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == UserRoles.TECHNICIAN

class IsDriver(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == UserRoles.DRIVER
    
class IsDispatcher(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == UserRoles.DISPATCHER
    
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == UserRoles.ADMIN

class IsCarrierManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == UserRoles.CARRIER_MANAGER

class UserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(
            {"user": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class UserLogin(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        user = serializer.validated_data['user']

        if not user:
            return Response(
                {"message": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access_token = response.data['access']
            refresh_token = response.data['refresh']
            
            cache.set(f"refresh_token_{user.id}", refresh_token, timeout=7*24*3600)
            
            _set_cookie(response, 'access_token', access_token, '/' ,15 * 60)
            _set_cookie(response, 'refresh_token', refresh_token, '/', 7 * 24 * 3600)

        return response


# @extend_schema(
#     request=TokenRefreshSerializer,
#     responses={200: TokenRefreshSerializer}
# )
class TokenRefresh(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response(
                {"error": "Refresh token missing"},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        try:
            refresh = RefreshToken(refresh_token)
            user_id = refresh['user_id']
            cached_refresh_token = cache.get(f"refresh_token_{user_id}")
            
            if not cached_refresh_token or cached_refresh_token != refresh_token:
                return Response(
                    {"error": "Invalid or expired refresh token"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
                
            request.data['refresh'] = refresh_token
            response = super().post(request, *args, **kwargs)
            
            if response.status_code == 200:
                new_access = response.data['access']
                new_refresh = response.data.get('refresh', refresh_token)

                if new_refresh:
                    cache.set(f"refresh_token_{user_id}", new_refresh, timeout=7 * 24 * 3600)
                    _set_cookie(response=response, key='refresh_token', value=new_refresh, path='/', max_age=7 *24 * 3600)

                _set_cookie(response=response, key='access_token', value=new_access, path='/', max_age=15 *60)
            
            return response
    
        except Exception as e:
            return Response(
                {"error": "Invalid refresh token"},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
            
class Logout(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        
        if not refresh_token:
            return Response(
                {"error": "Refresh token missing"},
                status.HTTP_401_UNAUTHORIZED
                )
            
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            user_id = request.user.id
            cache.delete(f"refresh_token_{user_id}")
            
            response = Response(
                {"message": 'Logged out sucessfully'},
                status=status.HTTP_200_OK,
            )
            response.delete_cookie("refresh_token")
            
            return response
        except TokenError as e:
            return Response(
                {"error": "Invalid refresh token"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserDetail(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Http404('User not found')

    def get(self, request):
        user = self.get_object(request.user.id)
        serializer = UserSerializer(user)
        
        return Response(
            {"user": serializer.data},
        )
        
    def delete(self, request):
        user = self.get_object(request.user.id)
        
        user.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
