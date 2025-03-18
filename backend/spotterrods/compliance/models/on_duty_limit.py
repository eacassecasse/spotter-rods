#!/usr/bin/python3
""" OnDutyLimit Module for SpotterRODS project """
from django.db import models
from core.models import BaseModel
from fleet.models import Driver


class OnDutyLimit(BaseModel):
    """ OnDutyLimit class """
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_7_day = models.BooleanField(default=True)
    total_hours = models.FloatField()
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='duty_limits')

    class Meta:
        db_table = 'duty_limits'
