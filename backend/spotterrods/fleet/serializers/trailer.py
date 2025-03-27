#!/usr/bin/python3
""" Trailer Serializer Module for SpotterRODS project """

from core.serializers import BaseSerializer
from .carrier import CarrierSerializer

from core.models import BaseModel
from ..models import Trailer


class TrailerSerializer(BaseSerializer):
    carrier = CarrierSerializer(read_only=True)

    class Meta:
        model = Trailer
        fields = ['id', 'number', 'in_use', 'carrier']
        related_serializers = {
            'carrier': 'fleet.serializers.CarrierSerializer'
        }
