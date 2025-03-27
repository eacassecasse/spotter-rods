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
from core.views import BaseViewMixin
from users.views import IsCarrierManager, IsAdmin


class CarrierList(generics.ListCreateAPIView, BaseViewMixin):
    queryset = Carrier.objects.all()
    serializer_class = CarrierSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'address']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCarrierManager() | IsAdmin()]
        return [IsAuthenticated()]
    


class CarrierDetail(generics.RetrieveUpdateDestroyAPIView, BaseViewMixin):
    queryset = Carrier.objects.all()
    serializer_class = CarrierSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsCarrierManager() | IsAdmin()]
        return [IsAuthenticated()]
