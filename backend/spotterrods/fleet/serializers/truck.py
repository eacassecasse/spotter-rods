#!/usr/bin/python3
""" Truck Serializer Module for SpotterRODS project """
from core.serializers import BaseSerializer
from . import CarrierSerializer

from core.models import BaseModel
from ..models import Truck


class TruckSerializer(BaseSerializer):
    carrier = CarrierSerializer(read_only=True)

    class Meta:
        model = Truck
        fields = ['id', 'brand', 'number', 'current_mileage', 'carrier']
