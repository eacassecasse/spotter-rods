#!/usr/bin/python3
""" Shipping View Module for SpotterRODS project """
from django.utils import timezone
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from core.models import BaseModel
from core.views import BaseViewMixin
from compliance.models import DutyStatus
from ..models import Shipping
from ..serializers import ShippingSerializer
from users.views import IsAdmin, IsDispatcher


class ShippingList(generics.ListCreateAPIView, BaseViewMixin):
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


class ShippingDetail(generics.RetrieveUpdateDestroyAPIView, BaseViewMixin):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsDispatcher() | IsAdmin()]
        return [IsAuthenticated()]
    
