#!/usr/bin/python3
""" Carrier Module for SpotterRODS project """
from django.db import models
from core.models import BaseModel
from users.models import User


class Carrier(BaseModel):
    """ Carrier class """
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    class Meta:
        db_table = 'carriers'
