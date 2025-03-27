#!/usr/bin/python3
""" DutyStatus Serializer Module for SpotterRODS project """
from rest_framework.exceptions import ValidationError
from core.serializers import BaseDutySerializer
from fleet.serializers import DriverSerializer

from core.models import BaseDuty
from ..models import DutyStatus


class DutyStatusSerializer(BaseDutySerializer):
    driver = DriverSerializer(read_only=True)

    class Meta:
        model = DutyStatus
        fields = ['id', 'status', 'location', 'driver']
        related_serializers = {
            'driver': 'fleet.serializers.DriverSerializer'
        }
        
    def validate_status(self, value):
        current_status = self.instance.status if self.instance else None
        if current_status == 'OFF_DUTY' and value == 'DRIVING':
            raise ValidationError("Cannot transition directly from OFF_DUTY to DRIVING.")
        return value
