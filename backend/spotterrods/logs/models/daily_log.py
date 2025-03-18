#!/usr/bin/python3
""" DailyLog module for the SpotterRODS project """
from django.db import models

from core.models import BaseModel
from fleet.models import Driver
from fleet.models import Truck
from fleet.models import Trailer
from shipping.models import Shipping


class DailyLog(BaseModel):
    """ DailyLog class """
    date = models.DateTimeField(auto_now_add=True)
    total_miles_driven = models.DecimalField(max_digits=14, decimal_places=2)
    shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE, related_name='daily_logs')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='daily_logs')
    truck = models.OneToOneField(Truck, on_delete=models.CASCADE, related_name='daily_logs')
    trailers = models.ManyToManyField(Trailer, related_name='daily_logs', blank=True)

    class Meta:
        db_table = 'daily_logs'
