#!/usr/bin/python3
""" Driver Serializer Module for SpotterRODS project """

import random
import string
from core.serializers import BaseSerializer
from users.serializers import UserSerializer
from . import CarrierSerializer
from core.models import BaseModel
from ..models import Driver
from users.models import UserRoles


class DriverSerializer(BaseSerializer):
    user = UserSerializer(read_only=True)
    carrier = CarrierSerializer(read_only=True)

    class Meta:
        model = Driver
        fields = ['id', 'name', 'license_number', 'total_mileage_driven', 'mileage_week', 'is_cdl_holder', 'carrier', 'user']
        related_serializers = {
            'carrier': 'fleet.serializers.CarrierSerializer'
        }
        
    def generate_username(self, name):
        """ Generates an username from the name of the driver """
        base = name.lower().replace(' ', '')
        random_suffix = ''.join(random.choices(string.digits, k=3))
        return '{}{}'.format(base, random_suffix)
    
    def create(self, validated_data):
        name = validated_data.get('name')
        
        
        username = self.generate_username(name)
        tmp_pwd = None
        
        user_data = {
            'username': username,
            'name': name,
            'role': UserRoles.DRIVER,
            'is_active': False
        }
        
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        
        validated_data['user'] = user
        driver = super().create(validated_data)
        
        return driver
