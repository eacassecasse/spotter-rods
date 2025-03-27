#!/usr/bin/python3
""" AdverseDrivingCondition Serializer Module for SpotterRODS project """
from core.serializers import BaseDutySerializer
from fleet.serializers import DriverSerializer

from core.models import BaseDuty
from ..models import AdverseDrivingCondition


class AdverseDrivingConditionSerializer(BaseDutySerializer):
    driver = DriverSerializer(read_only=True)

    class Meta:
        model = AdverseDrivingCondition
        fields = ['id', 'description', 'extended_driving_time', 'driver']
        related_serializers = {
            'driver': 'fleet.serializers.DriverSerializer'
        }
