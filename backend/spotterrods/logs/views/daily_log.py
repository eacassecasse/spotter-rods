#!/usr/bin/python3
""" DailyLog View Module for SpotterRODS project """
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from core.models import BaseModel
from core.views import BaseViewMixin
from ..models import DailyLog
from ..serializers import DailyLogSerializer
from users.views import IsDriver


class DailyLogList(generics.ListCreateAPIView, BaseViewMixin):
    queryset = DailyLog.objects.all()
    serializer_class = DailyLogSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['date']
    search_fields = ['date', 'total_miles_driven']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsDriver()]
        return [IsAuthenticated()]


class DailyLogDetail(generics.RetrieveUpdateDestroyAPIView, BaseViewMixin):
    queryset = DailyLog.objects.all()
    serializer_class = DailyLogSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsDriver()]
        return [IsAuthenticated()]
