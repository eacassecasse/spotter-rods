#!/usr/bin/python3
""" ShortHaulRemark Module for SpotterRODS project """
from django.db import models

from core.models import BaseModel
from .short_haul import ShortHaul


class ShortHaulRemark(BaseModel):
    """ A short haul exception remark model """
    short_haul = models.ForeignKey(ShortHaul, on_delete=models.CASCADE, related_name='short_haul_remarks')
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'short_haul_remarks'
