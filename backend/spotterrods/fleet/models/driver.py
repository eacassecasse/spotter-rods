#!/usr/bin/python3
""" Driver Module for SpotterRODS project """
from django.db import models
from core.models import BaseModel
from .carrier import Carrier
from users.models import User


class Driver(BaseModel):
    """ Driver class """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')
    name = models.CharField(max_length=105)
    license_number = models.CharField(max_length=21)
    total_mileage_driven = models.DecimalField(max_digits=14, decimal_places=2)
    mileage_week = models.DecimalField(max_digits=14, decimal_places=2)
    is_cdl_holder = models.BooleanField(default=False)
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE, related_name='drivers')

    class Meta:
        db_table = 'drivers'
