#!/usr/bin/python3
""" DutyRemark Module for SpotterRODS project """
from django.db import models

from core.models import BaseModel
from .duty_status import DutyStatus


class DutyRemark(BaseModel):
    """ A duty remark model """
    duty = models.ForeignKey(DutyStatus, on_delete=models.CASCADE, related_name='duty_remarks')
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'duty_remarks'
