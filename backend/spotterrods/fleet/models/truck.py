#!/usr/bin/python3
""" Truck Module for SpotterRODS project """
from django.db import models

from core.models import BaseModel
from .carrier import Carrier


class Truck(BaseModel):
    """ A carrier Trucks """
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)
    brand = models.CharField(max_length=50)
    current_mileage = models.DecimalField(max_digits=14, decimal_places=2, default=0.0)
    number = models.CharField(max_length=14)

    class Meta:
        db_table = 'trucks'
