#!/usr/bin/python3
"""This module defines a base class for all models in our project"""
import uuid
from datetime import datetime
from django.db import models


class BaseModel(models.Model):
    """A base class for all SpotterRODS models"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']
        
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def to_dict(self, exclude_fields=None):
        """Convert instance into dict format"""
        exclude_fields = exclude_fields or []
        dictionary = {
            'id': str(self.id),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'model_type': self.__class__.__name__
        }
        
        for field in self._meta.fields:
            if field.name not in exclude_fields + ['id', 'created_at', 'updated_at']:
                value = getattr(self, field.name)
                if hasattr(value, 'to_dict'):
                    dictionary[field.name] = value.to_dict()
                else:
                    dictionary[field.name] = value
        
        return dictionary
