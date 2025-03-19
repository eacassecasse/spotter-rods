#!/usr/bin/python3
""" Shipping Serializer Module for SpotterRODS project """
from core.serializers import BaseSerializer
from fleet.serializers import CarrierSerializer

from core.models import BaseModel
from ..models import Shipping


class ShippingSerializer(BaseSerializer):
    carrier = CarrierSerializer(read_only=True)

    class Meta:
        model = Shipping
        fields = ['id', 'number', 'commodity', 'carrier']
