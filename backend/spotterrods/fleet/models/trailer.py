#!/usr/bin/python3
""" Trailer Module for SpotterRODS project """
from django.db import models

from core.models import BaseModel
from .carrier import Carrier


class Trailer(BaseModel):
    """ A carrier Trailers """
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)
    number = models.CharField(max_length=14)
    in_use = models.BooleanField(default=False)

    class Meta:
        db_table = 'trailers'
