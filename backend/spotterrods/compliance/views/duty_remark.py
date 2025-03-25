#!/usr/bin/python3
""" DutyRemark View Module for SpotterRODS project """
from django.utils import timezone
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from core.models import BaseModel
from users.models import UserRoles
from ..models import DutyRemark, DutyStatus
from ..serializers import DutyRemarkSerializer
from users.views import IsDriver, IsDispatcher, IsAdmin


class DutyRemarkList(generics.ListCreateAPIView):
    queryset = DutyRemark.objects.all()
    serializer_class = DutyRemarkSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['description']
    search_fields = ['description']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsDriver()]
        return [IsAuthenticated(), IsDriver(), IsDispatcher(), IsAdmin()]
    
    def perform_create(self, serializer):
        duty_status = DutyStatus.objects.filter(
            driver=self.request.user
        ).order_by('-start_at').first()
        if not duty_status:
            raise ValidationError('No active duty status found for this driver')
        serializer.save(duty=duty_status)
    
    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response(
                {"error": "You do not have the permission to perfom this action"},
                status=status.HTTP_403_FORBIDDEN
            )
        elif isinstance(exc, ValidationError):
            return Response(
                {"error": "FMCSA violation", "details": exc.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().handle_exception(exc)


class DutyRemarkDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DutyRemarkSerializer
    
    def get_queryset(self):
        if self.request.user.role == UserRoles.DRIVER:
            return DutyRemark.objects.filter(duty__driver=self.request.user)
        return DutyRemark.objects.all()
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsDriver()]
        return [IsAuthenticated(), IsDriver(), IsDispatcher(), IsAdmin()]
    
    def perform_update(self, serializer):
        remark = self.get_object()
        if (timezone.now() - remark.created_at).days >= 1:
            raise ValidationError("Cannot modify entries older than 24 hours.")
        serializer.save()
    
    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response(
                {"error": "You do not have the permission to perfom this action"},
                status=status.HTTP_403_FORBIDDEN
            )
        elif isinstance(exc, ValidationError):
            return Response(
                {"error": "FMCSA violation", "details": exc.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().handle_exception(exc)
