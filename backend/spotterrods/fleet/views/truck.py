#!/usr/bin/python3
""" Truck View Module for SpotterRODS project """
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from core.models import BaseModel
from core.views import BaseViewMixin
from ..models import Truck
from ..serializers import TruckSerializer
from users.views import IsCarrierManager, IsAdmin


class TruckList(generics.ListCreateAPIView, BaseViewMixin):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['brand']
    search_fields = ['brand', 'current_mileage', 'number']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCarrierManager() | IsAdmin()]
        return [IsAuthenticated()]


class TruckDetail(generics.RetrieveUpdateDestroyAPIView, BaseViewMixin):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsCarrierManager() | IsAdmin()]
        return [IsAuthenticated()]
