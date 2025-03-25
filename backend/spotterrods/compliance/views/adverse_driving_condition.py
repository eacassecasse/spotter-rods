#!/usr/bin/python3
""" AdverseDrivingCondition View Module for SpotterRODS project """
from django.utils import timezone
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from core.models import BaseModel
from users.models import UserRoles
from ..models import AdverseDrivingCondition
from ..serializers import AdverseDrivingConditionSerializer
from users.views import IsDriver, IsDispatcher, IsAdmin

class AdverseDrivingConditionList(generics.ListCreateAPIView):
    queryset = AdverseDrivingCondition.objects.all()
    serializer_class = AdverseDrivingConditionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['description']
    search_fields = ['description', 'extended_driving_time']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsDriver()]
        return [IsAuthenticated(), IsDriver(), IsDispatcher(), IsAdmin()]
    
    def perform_create(self, serializer):
        serializer.save(driver=self.request.user, start_at=timezone.now())
    
    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response(
                {"error": "You do not have the permission to perfom this action"},
                status=status.HTTP_403_FORBIDDEN
            )
        elif isinstance(exc, ValidationError):
            return Response(
                {"error": "FCMSA violation", "details": exc.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().handle_exception(exc)


class AdverseDrivingConditionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdverseDrivingConditionSerializer
    
    def get_queryset(self):
        if self.request.user.role == UserRoles.DRIVER:
            return AdverseDrivingCondition.objects.filter(driver=self.request.user)
        return AdverseDrivingCondition.objects.all()
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsDriver()]
        return [IsAuthenticated(), IsDriver(), IsDispatcher(), IsAdmin()]
    
    def perform_update(self, serializer):
        if (timezone.now() - self.get_object().start_at).days >= 1:
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
                {"error": "FMCSA", "details": exc.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().handle_exception(exc)
