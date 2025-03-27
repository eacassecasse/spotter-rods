#!/usr/bin/python3
""" DutyRemark Serializer Module for SpotterRODS project """
from core.serializers import BaseSerializer
from .duty_status import DutyStatusSerializer

from core.models import BaseModel
from ..models import DutyRemark


class DutyRemarkSerializer(BaseSerializer):
    duty = DutyStatusSerializer(read_only=True)

    class Meta:
        model = DutyRemark
        fields = ['id', 'description', 'duty']
        related_serializers = {
            'duty': 'compliance.serializers.DutyStatusSerializer'
        }
