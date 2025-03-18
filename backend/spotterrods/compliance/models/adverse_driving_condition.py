#!/usr/bin/python3
""" AdverseDrivingCondition Module for SpotterRODS project """
from django.db import models
from core.models import BaseDuty
from fleet.models import Driver


class AdverseDrivingCondition(BaseDuty):
    """ AdverseDrivingCondition class """
    description = models.TextField()
    extended_driving_time = models.FloatField()
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='adverse_driving_conditions')

    class Meta:
        db_table = 'adverse_driving_conditions'
