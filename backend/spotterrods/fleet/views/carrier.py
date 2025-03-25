#!/usr/bin/python3
""" Carrier View Module for SpotterRODS project """
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError

from core.models import BaseModel
from ..models import Carrier
from ..serializers import CarrierSerializer
from users.views import IsCarrierManager, IsAdmin


class CarrierList(generics.ListCreateAPIView):
    queryset = Carrier.objects.all()
    serializer_class = CarrierSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'address']

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


class CarrierDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Carrier.objects.all()
    serializer_class = CarrierSerializer
    
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
