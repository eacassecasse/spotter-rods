#!/usr/bin/python3
""" Trailer View Module for SpotterRODS project """
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from core.models import BaseModel
from core.views import BaseViewMixin
from ..models import Trailer
from ..serializers import TrailerSerializer
from users.views import IsAdmin, IsCarrierManager


class TrailerList(generics.ListCreateAPIView, BaseViewMixin):
    queryset = Trailer.objects.all()
    serializer_class = TrailerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['number']
    search_fields = ['number', 'in_use']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCarrierManager() | IsAdmin()]
        return [IsAuthenticated()]


class TrailerDetail(generics.RetrieveUpdateDestroyAPIView, BaseViewMixin):
    queryset = Trailer.objects.all()
    serializer_class = TrailerSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsCarrierManager() | IsAdmin()]
        return [IsAuthenticated()]
