#!/usr/bin/python3
""" SleeperBerth Serializer Module for SpotterRODS project """
from core.serializers import BaseDutySerializer
from fleet.serializers import DriverSerializer

from core.models import BaseDuty
from ..models import SleeperBerth


class SleeperBerthSerializer(BaseDutySerializer):
    driver = DriverSerializer(read_only=True)

    class Meta:
        model = SleeperBerth
        fields = ['id', 'is_qualified', 'driver']
