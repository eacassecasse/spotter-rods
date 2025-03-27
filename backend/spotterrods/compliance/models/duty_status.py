#!/usr/bin/python3
""" DutyStatus Module for SpotterRODS project """
from enum import Enum
from django.db import models
from django.core.validators import MinLengthValidator
from rest_framework.exceptions import ValidationError
from core.models import BaseDuty
from fleet.models import Driver


class DutyStatusChoice(Enum):
    OFF_DUTY = 'OFF_DUTY'
    ON_DUTY = 'ON_DUTY'
    DRIVING = 'DRIVING'
    SLEEPER_BERTH = 'SLEEPER_BERTH'
    
    @classmethod
    def choices(cls):
        return [(key.value, key.name.replace('_', ' ')) for key in cls]
    

class DutyStatus(BaseDuty):
    """ DutyStatus class """
    status = models.CharField(max_length=15, choices=DutyStatusChoice.choices(), db_index=True)
    location = models.CharField(max_length=95, validators=[MinLengthValidator(3)])
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='duty_statuses')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['driver', 'end_at'],
                condition=models.Q(end_at__isnull=True),
                name='unique_active_status_per_driver'
            )
        ]
        db_table = 'duty_statuses'
        
    def validate_status_transition(self, new_status):
        """ Validate transition between statuses"""
        valid_transitions = {
            DutyStatusChoice.OFF_DUTY.value: [DutyStatusChoice.ON_DUTY.value],
            DutyStatusChoice.ON_DUTY.value: [
                DutyStatusChoice.DRIVING.value,
                DutyStatusChoice.OFF_DUTY.value,
                DutyStatusChoice.SLEEPER_BERTH.value
            ],
        }
        
        if self.status and self.status not in valid_transitions.get(new_status, []):
            raise ValidationError(f"Invalid status transition from {self.status} to {new_status}")
    
    def save(self, *args, **kwargs):
        if self.pk:
            original = DutyStatus.objects.get(pk=self.pk)
            self.validate_status_transition(self.status)
        super().save(*args, *kwargs)
