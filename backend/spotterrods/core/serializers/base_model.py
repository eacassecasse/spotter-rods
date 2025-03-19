#!/usr/bin/python3
""" Base Serializer Module for SpotterRODS project """
from rest_framework import serializers

from ..models import BaseModel


class BaseSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
