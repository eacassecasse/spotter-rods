#!/usr/bin/python3
""" OnDutyLimit Serializer Module for SpotterRODS project """
from core.serializers import BaseSerializer
from fleet.serializers import DriverSerializer

from core.models import BaseModel
from ..models import OnDutyLimit


class OnDutyLimitSerializer(BaseSerializer):
    driver = DriverSerializer(read_only=True)

    class Meta:
        model = OnDutyLimit
        fields = ['id', 'start_date', 'end_date', 'is_7_day', 'total_hours', 'driver']
