#!/usr/bin/python3
""" AdverseDrivingCondition View Module for SpotterRODS project """
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.models import BaseModel
from ..models import AdverseDrivingCondition
from ..serializers import AdverseDrivingConditionSerializer


class AdverseDrivingConditionList(generics.ListCreateAPIView):
    queryset = AdverseDrivingCondition.objects.all()
    serializer_class = AdverseDrivingConditionSerializer
    permission_classes = [IsAuthenticated]


class AdverseDrivingConditionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdverseDrivingCondition.objects.all()
    serializer_class = AdverseDrivingConditionSerializer
    permission_classes = [IsAuthenticated]
