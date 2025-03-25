#!/usr/bin/python3
""" Shipping View Module for SpotterRODS project """
from django.utils import timezone
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from core.models import BaseModel
from compliance.models import DutyStatus
from ..models import Shipping
from ..serializers import ShippingSerializer
from users.views import IsAdmin, IsDispatcher


class ShippingList(generics.ListCreateAPIView):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['number']
    search_fields = ['number', 'commodity']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsDispatcher() | IsAdmin()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        driver = serializer.validated_data['driver']
        if not DutyStatus.objects.filter(driver=driver, status='ON_DUTY').exists():
            raise ValidationError("Driver must be ON_DUTY to assign shipment.")
        serializer.save()
    
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


class ShippingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsDispatcher() | IsAdmin()]
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
