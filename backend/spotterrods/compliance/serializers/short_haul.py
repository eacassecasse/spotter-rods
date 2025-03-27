#!/usr/bin/python3
""" ShortHaul Serializer Module for SpotterRODS project """
from core.serializers import BaseSerializer
from fleet.serializers import DriverSerializer

from core.models import BaseModel
from ..models import ShortHaul


class ShortHaulSerializer(BaseSerializer):
    driver = DriverSerializer(read_only=True)

    class Meta:
        model = ShortHaul
        fields = ['id', 'date', 'is_cdl', 'radius_miles', 'return_time', 'description', 'driver']
        related_serializers = {
            'driver': 'fleet.serializers.DriverSerializer'
        }
