#!/usr/bin/python3
""" Sleeper Berth Module for SpotterRODS project """
from django.db import models
from core.models import BaseDuty
from fleet.models import Driver


class SleeperBerth(BaseDuty):
    """ SleeperBerth class """
    is_qualified = models.BooleanField(default=False)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='sleeper_berths')

    class Meta:
        db_table = 'sleeper_berths'
