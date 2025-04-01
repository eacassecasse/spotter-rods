#!/usr/bin/python
""" Password Setup View for SpotterRODS Project"""

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from ..models import User
from ..serializers import UserSerializer

class PasswordSetupView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        
        if 'password' not in request.data:
            raise ValidationError('Password is required')
        
        password = request.data["password"]
        user.set_password(password)
        user.is_active = True
        user.save()
        
        return Response(
            {"message": "Password set successfully"},
            status=status.HTTP_200_OK
        )
