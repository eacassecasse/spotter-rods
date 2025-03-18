#!/usr/bin/python3
""" Restart Module for SpotterRODS project """
from django.db import models
from core.models import BaseDuty
from fleet.models import Driver


class Restart(BaseDuty):
    """ Restart class """
    is_complete = models.BooleanField(default=False)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='restarts')

    class Meta:
        db_table = 'restarts'
