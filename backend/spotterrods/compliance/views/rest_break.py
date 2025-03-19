#!/usr/bin/python3
""" RestBreak View Module for SpotterRODS project """
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.models import BaseModel
from ..models import RestBreak
from ..serializers import RestBreakSerializer


class RestBreakList(generics.ListCreateAPIView):
    queryset = RestBreak.objects.all()
    serializer_class = RestBreakSerializer
    permission_classes = [IsAuthenticated]


class RestBreakDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RestBreak.objects.all()
    serializer_class = RestBreakSerializer
    permission_classes = [IsAuthenticated]
