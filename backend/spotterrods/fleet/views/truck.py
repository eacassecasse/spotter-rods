#!/usr/bin/python3
""" Truck View Module for SpotterRODS project """
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from core.models import BaseModel
from ..models import Truck
from ..serializers import TruckSerializer
from users.views import IsCarrierManager, IsAdmin


class TruckList(generics.ListCreateAPIView):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['brand']
    search_fields = ['brand', 'current_mileage', 'number']

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


class TruckDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer
    
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
