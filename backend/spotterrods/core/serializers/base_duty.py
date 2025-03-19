#!/usr/bin/python3
""" Base Duty Serializer Module for SpotterRODS project """
from rest_framework import serializers

from . import BaseSerializer


class BaseDutySerializer(BaseSerializer):
    start_at = serializers.DateTimeField()
    end_at = serializers.DateTimeField()
