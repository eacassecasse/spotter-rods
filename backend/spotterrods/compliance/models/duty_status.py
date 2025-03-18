#!/usr/bin/python3
""" DutyStatus Module for SpotterRODS project """
from django.db import models
from core.models import BaseDuty
from fleet.models import Driver


STATUS_CHOICES = [
    ('OFF_DUTY', 'Off Duty'),
    ('ON_DUTY', 'On Duty'),
    ('DRIVING', 'Driving'),
    ('SLEEPER_BERTH', 'Sleeper Berth')
    ]

class DutyStatus(BaseDuty):
    """ DutyStatus class """
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, db_index=True)
    location = models.CharField(max_length=95)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='duty_statuses')

    class Meta:
        db_table = 'duty_statuses'
