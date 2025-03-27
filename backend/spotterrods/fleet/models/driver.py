#!/usr/bin/python3
""" Driver Module for SpotterRODS project """
from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator
from rest_framework.exceptions import ValidationError
from core.models import BaseModel
from .carrier import Carrier
from users.models import User


class Driver(BaseModel):
    """ Driver class """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    name = models.CharField(max_length=105)
    license_number = models.CharField(max_length=21, unique=True, validators=[RegexValidator(r'^[A-Z0-9]+$')])
    total_mileage_driven = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    mileage_week = models.DecimalField(max_digits=14, decimal_places=2)
    is_cdl_holder = models.BooleanField(default=False)
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE, related_name='drivers')
    
    @property
    def active_duty_status(self):
        """" Get the current duty status"""
        return self.duty_statuses.filter(end_at__isnull=True).first()
    
    def clean(self):
        """Model-level validation"""
        if self.is_cdl_holder and len(self.license_number) != 12:
            raise ValidationError("CDL holders must have 12-character license numbers")

    class Meta:
        db_table = 'drivers'
