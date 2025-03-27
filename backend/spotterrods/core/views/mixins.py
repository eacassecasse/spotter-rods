#!/usr/bin/python3

from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, PermissionDenied

class BaseViewMixin:
    """Common view functionality for all API views"""
    
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
    
    def get_serializer_context(self):
        """Add common context to all serializers"""
        context = super().get_serializer_context()
        context.update({
            'request': self.request,
            'view': self,
            'format': self.format_kwarg
        })
        return context
