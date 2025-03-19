#!/usr/bin/python3
""" DutyStatus View Module for SpotterRODS project """
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.models import BaseModel
from ..models import DutyStatus
from ..serializers import DutyStatusSerializer


class DutyStatusList(generics.ListCreateAPIView):
    queryset = DutyStatus.objects.all()
    serializer_class = DutyStatusSerializer
    permission_classes = [IsAuthenticated]


class DutyStatusDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DutyStatus.objects.all()
    serializer_class = DutyStatusSerializer
    permission_classes = [IsAuthenticated]
