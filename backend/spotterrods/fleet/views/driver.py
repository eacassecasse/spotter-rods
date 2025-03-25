#!/usr/bin/python3
""" Driver View Module for SpotterRODS project """
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from core.models import BaseModel
from ..models import Driver
from users.views import IsCarrierManager, IsAdmin
from ..serializers import DriverSerializer


class DriverList(generics.ListCreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'license_number', 'is_cdl_holder']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCarrierManager() | IsAdmin()]
        return [IsAuthenticated()]
    
    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response(
                {"error": "You do not have the permission to perfom this action"},
                status=status.HTTP_403_FORBIDDEN
            )
        elif isinstance(exc, ValidationError):
            return Response(
                {"error": "Invalid input", "details": exc.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().handle_exception(exc)


class DriverDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsCarrierManager() | IsAdmin()]
        return [IsAuthenticated()]
    
    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response(
                {"error": "You do not have the permission to perfom this action"},
                status=status.HTTP_403_FORBIDDEN
            )
        elif isinstance(exc, ValidationError):
            return Response(
                {"error": "Invalid input", "details": exc.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().handle_exception(exc)
