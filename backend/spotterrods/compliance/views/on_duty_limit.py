#!/usr/bin/python3
""" OnDutyLimit View Module for SpotterRODS project """
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.models import BaseModel
from ..models import OnDutyLimit
from ..serializers import OnDutyLimitSerializer


class OnDutyLimitList(generics.ListCreateAPIView):
    queryset = OnDutyLimit.objects.all()
    serializer_class = OnDutyLimitSerializer
    permission_classes = [IsAuthenticated]


class OnDutyLimitDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OnDutyLimit.objects.all()
    serializer_class = OnDutyLimitSerializer
    permission_classes = [IsAuthenticated]
