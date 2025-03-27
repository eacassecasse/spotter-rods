#!/usr/bin/python3
""" Driver View Module for SpotterRODS project """
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from core.models import BaseModel
from core.views import BaseViewMixin
from ..models import Driver
from users.views import IsCarrierManager, IsAdmin
from ..serializers import DriverSerializer


class DriverList(generics.ListCreateAPIView, BaseViewMixin):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'license_number', 'is_cdl_holder']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCarrierManager() | IsAdmin()]
        return [IsAuthenticated()]


class DriverDetail(generics.RetrieveUpdateDestroyAPIView, BaseViewMixin):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsCarrierManager() | IsAdmin()]
        return [IsAuthenticated()]
