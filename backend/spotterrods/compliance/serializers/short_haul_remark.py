#!/usr/bin/python3
""" ShortHaulRemark Serializer Module for SpotterRODS project """
from core.serializers import BaseSerializer
from .short_haul import ShortHaulSerializer

from core.models import BaseModel
from ..models import ShortHaulRemark


class ShortHaulRemarkSerializer(BaseSerializer):
    short_haul = ShortHaulSerializer(read_only=True)

    class Meta:
        model = ShortHaulRemark
        fields = ['id', 'description', 'short_haul']
