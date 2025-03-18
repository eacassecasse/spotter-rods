#!/usr/bin/python3
""" ShortHaul Modules for SpotterRODS project """
from django.db import models
from core.models import BaseModel
from fleet.models import Driver


class ShortHaul(BaseModel):
    """ ShortHaul class """
    date = models.DateTimeField()
    is_cdl = models.BooleanField(default=False)
    radius_miles = models.FloatField()
    return_time = models.DateTimeField()
    description = models.TextField()
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='short_haul_exceptions')

    class Meta:
        db_table = 'short_haul_exceptions'
