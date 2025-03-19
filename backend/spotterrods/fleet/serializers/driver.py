#!/usr/bin/python3
""" Driver Serializer Module for SpotterRODS project """

from core.serializers import BaseSerializer
from users.serializers import UserSerializer
from . import CarrierSerializer

from core.models import BaseModel

from ..models import Driver


class DriverSerializer(BaseSerializer):
    user = UserSerializer(read_only=True)
    carrier = CarrierSerializer(read_only=True)

    class Meta:
        model = Driver
        fields = ['id', 'name', 'license_number', 'total_mileage_driven', 'mileage_week', 'is_cdl_holder', 'carrier', 'user']
