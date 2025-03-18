#!/usr/bin/python3
""" Shipping Module for SpotterRODS project """
from django.db import models

from core.models import BaseModel
from fleet.models import Carrier


class Shipping(BaseModel):
    """ A carrier Shippings """
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)
    number = models.CharField(max_length=14)
    commodity = models.CharField(max_length=255)

    class Meta:
        db_table = 'shippings'
