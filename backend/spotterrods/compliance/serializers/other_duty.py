#!/usr/bin/python3
""" OtherDuty Serializer Module for SpotterRODS project """
from core.serializers import BaseDutySerializer
from fleet.serializers import DriverSerializer

from core.models import BaseDuty
from ..models import OtherDuty


class OtherDutySerializer(BaseDutySerializer):
    driver = DriverSerializer(read_only=True)

    class Meta:
        model = OtherDuty
        fields = ['id', 'type', 'location', 'driver']
