#!/usr/bin/python3
""" ShortHaul View Module for SpotterRODS project """
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.models import BaseModel
from ..models import ShortHaul
from ..serializers import ShortHaulSerializer


class ShortHaulList(generics.ListCreateAPIView):
    queryset = ShortHaul.objects.all()
    serializer_class = ShortHaulSerializer
    permission_classes = [IsAuthenticated]


class ShortHaulDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShortHaul.objects.all()
    serializer_class = ShortHaulSerializer
    permission_classes = [IsAuthenticated]
