#!/usr/bin/python3
""" DailyLog View Module for SpotterRODS project """
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from core.models import BaseModel
from ..models import DailyLog
from ..serializers import DailyLogSerializer
from users.views import IsDriver


class DailyLogList(generics.ListCreateAPIView):
    queryset = DailyLog.objects.all()
    serializer_class = DailyLogSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['date']
    search_fields = ['date', 'total_miles_driven']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsDriver()]
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


class DailyLogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DailyLog.objects.all()
    serializer_class = DailyLogSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsDriver()]
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
