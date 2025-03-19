#!/usr/bin/python3
""" OtherDuty View Module for SpotterRODS project """
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.models import BaseModel
from ..models import OtherDuty
from ..serializers import OtherDutySerializer


class OtherDutyList(generics.ListCreateAPIView):
    queryset = OtherDuty.objects.all()
    serializer_class = OtherDutySerializer
    permission_classes = [IsAuthenticated]


class OtherDutyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OtherDuty.objects.all()
    serializer_class = OtherDutySerializer
    permission_classes = [IsAuthenticated]
