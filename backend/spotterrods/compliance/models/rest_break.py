#!/usr/bin/python3
""" Quiz Module for EduAccess project """
from django.db import models
from core.models import BaseDuty
from fleet.models import Driver

TYPE_CHOICES = [
    ('OFF_DUTY', 'Off Duty'),
    ('ON_DUTY', 'On Duty Not Driving'),
    ('SLEEPER_BERTH', 'Sleeper Berth')]

class RestBreak(BaseDuty):
    """ RestBreak class """
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='rest_breaks')

    class Meta:
        db_table = 'rest_breaks'
