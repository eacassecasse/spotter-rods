#!/usr/bin/python3
""" RestBreak Serializer Module for SpotterRODS project """
from core.serializers import BaseDutySerializer
from fleet.serializers import DriverSerializer

from core.models import BaseDuty
from ..models import RestBreak


class RestBreakSerializer(BaseDutySerializer):
    driver = DriverSerializer(read_only=True)

    class Meta:
        model = RestBreak
        fields = ['id', 'type', 'driver']
