#!/usr/bin/python3
""" OtherDuty Module for SpotterRODS project """
from django.db import models
from core.models import BaseDuty
from fleet.models import Driver


TYPE_CHOICES = [
    ('PERSONAL_CONVEYANCE', 'Personal Conveyance'),
    ('YARD_MOVE', 'Yard Move')
]
class OtherDuty(BaseDuty):
    """ OtherDuty class """
    location = models.CharField(max_length=95)
    type = models.CharField(max_length=25, choices=TYPE_CHOICES)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='other_duties')

    class Meta:
        db_table = 'other_duties'
