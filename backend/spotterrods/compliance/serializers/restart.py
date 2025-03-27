#!/usr/bin/python3
""" Restart Serializer Module for SpotterRODS project """
from core.serializers import BaseDutySerializer
from fleet.serializers import DriverSerializer

from core.models import BaseDuty
from ..models import Restart


class RestartSerializer(BaseDutySerializer):
    driver = DriverSerializer(read_only=True)

    class Meta:
        model = Restart
        fields = ['id', 'is_completed', 'driver']
        related_serializers = {
            'driver': 'fleet.serializers.DriverSerializer'
        }
