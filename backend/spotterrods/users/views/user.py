#!/usr/bin/python3
""" User View Module for SpotterRODS project """
from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.http import Http404

from core.models import BaseModel
from ..models import User, UserRoles
from ..serializers import UserSerializer, UserLoginSerializer


def _set_cookie(response, refresh_token):
    response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="Strict"
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
    permission_classes = [IsTechnician]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(
            {"user": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class UserLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(request, username=username, password=password)

        if not user:
            return Response(
                {"message": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        cache.set(f"refresh_token_{user.id}", refresh_token, timeout=7 * 24 * 3600)

        response = Response(
            { "access_token": access_token, "refresh_token": refresh_token },
            status=status.HTTP_200_OK
            )

        _set_cookie(response=response, refresh_token=refresh_token)

        return response


class TokenRefresh(APIView):
    def post(self, request):
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
                    {"error": ""},
                    status=status.HTTP_401_UNAUTHORIZED
                )
                
            new_access_token = str(refresh.access_token)
            new_refresh_token = str(refresh)

            cache.set(f"refresh_token_{user_id}", new_refresh_token, timeout=7 * 24 * 3600)

            response = Response(
                { "access_token": new_access_token, "refresh_token": new_refresh_token },
                status=status.HTTP_200_OK
            )

            _set_cookie(response=response, refresh_token=new_access_token)
            
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
                {"message": "Logged out successfully"},
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
