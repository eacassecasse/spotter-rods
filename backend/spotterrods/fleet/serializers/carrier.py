#!/usr/bin/python3
""" Carrier Serializer Module for SpotterRODS project """
from rest_framework import serializers
from core.serializers import BaseSerializer

from core.models import BaseModel
from ..models import Carrier


class CarrierSerializer(BaseSerializer):
    class Meta:
        model = Carrier
        fields = ['id', 'name', 'address']
