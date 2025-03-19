#!/usr/bin/python3
""" Trailer View Module for SpotterRODS project """
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.models import BaseModel
from ..models import Trailer
from ..serializers import TrailerSerializer


class TrailerList(generics.ListCreateAPIView):
    queryset = Trailer.objects.all()
    serializer_class = TrailerSerializer
    permission_classes = [IsAuthenticated]


class TrailerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trailer.objects.all()
    serializer_class = TrailerSerializer
    permission_classes = [IsAuthenticated]
