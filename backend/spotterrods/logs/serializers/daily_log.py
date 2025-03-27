#!/usr/bin/python3
""" DailyLog Serializer Module for SpotterRODS project """
from core.serializers import BaseSerializer
from fleet.serializers import TruckSerializer
from fleet.serializers import DriverSerializer
from shipping.serializers import ShippingSerializer

from core.models import BaseModel
from ..models import DailyLog


class DailyLogSerializer(BaseSerializer):
    truck = TruckSerializer(read_only=True)
    driver = DriverSerializer(read_only=True)
    shipping = ShippingSerializer(read_only=True)

    class Meta:
        model = DailyLog
        fields = ['id', 'date', 'total_miles_driven', 'driver', 'truck', 'shipping']
        related_serializers = {
            'driver': 'fleet.serializers.DriverSerializer',
            'truck': 'fleet.serializers.TruckSerializer',
            'shipping': 'shipping.serializer.ShippingSerializer'
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if 'include' in request.GET and 'trailers' in request.GET['include']:
            from fleet.serializers import TrailerSerializer
            representation['trailers'] = TrailerSerializer(
                instance.trailers.all(),many=True, read_only=True)

            return representation
