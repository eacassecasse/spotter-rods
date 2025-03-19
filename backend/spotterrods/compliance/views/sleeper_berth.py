#!/usr/bin/python3
""" SleeperBerth View Module for SpotterRODS project """
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.models import BaseModel
from ..models import SleeperBerth
from ..serializers import SleeperBerthSerializer


class SleeperBerthList(generics.ListCreateAPIView):
    queryset = SleeperBerth.objects.all()
    serializer_class = SleeperBerthSerializer
    permission_classes = [IsAuthenticated]


class SleeperBerthDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SleeperBerth.objects.all()
    serializer_class = SleeperBerthSerializer
    permission_classes = [IsAuthenticated]
