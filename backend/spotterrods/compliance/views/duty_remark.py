#!/usr/bin/python3
""" DutyRemark View Module for SpotterRODS project """
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.models import BaseModel
from ..models import DutyRemark
from ..serializers import DutyRemarkSerializer


class DutyRemarkList(generics.ListCreateAPIView):
    queryset = DutyRemark.objects.all()
    serializer_class = DutyRemarkSerializer
    permission_classes = [IsAuthenticated]


class DutyRemarkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DutyRemark.objects.all()
    serializer_class = DutyRemarkSerializer
    permission_classes = [IsAuthenticated]
