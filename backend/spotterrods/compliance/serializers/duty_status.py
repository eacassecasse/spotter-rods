#!/usr/bin/python3
""" DutyStatus Serializer Module for SpotterRODS project """
from core.serializers import BaseDutySerializer
from fleet.serializers import DriverSerializer

from core.models import BaseDuty
from ..models import DutyStatus


class DutyStatusSerializer(BaseDutySerializer):
    driver = DriverSerializer(read_only=True)

    class Meta:
        model = DutyStatus
        fields = ['id', 'status', 'location', 'driver']
