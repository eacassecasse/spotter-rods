#!/usr/bin/python3
"""This module defines a base class for duty models in our project"""
from datetime import datetime
from django.db import models
from .base_model import BaseModel

class BaseDuty(BaseModel):
    """A base class for all SpotterRODS duties"""
    start_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(null=False, blank=True)

    class Meta:
        abstract = True
