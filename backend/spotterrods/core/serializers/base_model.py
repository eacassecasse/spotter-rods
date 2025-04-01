#!/usr/bin/python3
""" Base Serializer Module for SpotterRODS project """
from rest_framework import serializers
from importlib import import_module
from django.utils.module_loading import import_string
from ..models import BaseModel


class BaseSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%dT%H:%M:%SZ')
    updated_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%dT%H:%M:%SZ')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_field_serializers()
        
    def setup_field_serializers(self):
        """Configure dynamic serializers for related fields"""
        if hasattr(self.Meta, 'related_serializers'):
            for field_name, serializer_path in self.Meta.related_serializers.items():
                if field_name in self.fields:
                    try:
                        serializer_class = import_string(serializer_path)
                        self.fields[field_name] = serializer_class(read_only=True)
                    except ImportError as e:
                        raise ImportError(f"Could not import serializer '{serializer_path}' for field '{field_name}'. {str(e)}")
                    
    def validate(self, data):
        """Global validation hook"""
        data = super().validate(data)
        return data
