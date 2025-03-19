#!/usr/bin/python3
""" Restart View Module for SpotterRODS project """
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.models import BaseModel
from ..models import Restart
from ..serializers import RestartSerializer


class RestartList(generics.ListCreateAPIView):
    queryset = Restart.objects.all()
    serializer_class = RestartSerializer
    permission_classes = [IsAuthenticated]


class RestartDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restart.objects.all()
    serializer_class = RestartSerializer
    permission_classes = [IsAuthenticated]
