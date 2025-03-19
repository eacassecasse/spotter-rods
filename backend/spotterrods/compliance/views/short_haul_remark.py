#!/usr/bin/python3
""" ShortHaulRemark View Module for SpotterRODS project """
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.models import BaseModel
from ..models import ShortHaulRemark
from ..serializers import ShortHaulRemarkSerializer


class ShortHaulRemarkList(generics.ListCreateAPIView):
    queryset = ShortHaulRemark.objects.all()
    serializer_class = ShortHaulRemarkSerializer
    permission_classes = [IsAuthenticated]


class ShortHaulRemarkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShortHaulRemark.objects.all()
    serializer_class = ShortHaulRemarkSerializer
    permission_classes = [IsAuthenticated]
