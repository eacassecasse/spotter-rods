#!/usr/bin/python3
""" Carrier View Module for SpotterRODS project """
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated, BasePermission

from core.models import BaseModel
from ..models import Carrier
from ..serializers import CarrierSerializer
from users.models import UserRoles


class IsTechnician(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == UserRoles.TECHNICIAN


class CarrierList(generics.ListCreateAPIView):
    queryset = Carrier.objects.all()
    serializer_class = CarrierSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'address']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsTechnician()]
        return [IsAuthenticated()]


class CarrierDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Carrier.objects.all()
    serializer_class = CarrierSerializer
    permission_classes = [IsAuthenticated]
