#!/usr/bin/python3
""" DailyLog View Module for SpotterRODS project """
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.models import BaseModel
from ..models import DailyLog
from ..serializers import DailyLogSerializer


class DailyLogList(generics.ListCreateAPIView):
    queryset = DailyLog.objects.all()
    serializer_class = DailyLogSerializer
    permission_classes = [IsAuthenticated]


class DailyLogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DailyLog.objects.all()
    serializer_class = DailyLogSerializer
    permission_classes = [IsAuthenticated]
