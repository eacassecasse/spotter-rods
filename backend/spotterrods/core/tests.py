#!/usr/bin/python3

import uuid
from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from core.models import BaseDuty
from fleet.models import Driver, Carrier
from compliance.models import DutyStatus
from users.models import User, UserRoles

class BaseDutyTest(TestCase):
    def setUp(self):
        self.carrier = Carrier.objects.create(name="Turbo Jet")
        self.user = User.objects.create(
            username='edmilsoncassecasse',
            password='testpass123',
            name='Test User',
            role=UserRoles.DRIVER
        )
        self.driver = Driver.objects.create(
            name="Edmilson Cassecasse",
            license_number="DL12345678",
            total_mileage_driven=0,
            mileage_week=0,
            carrier=self.carrier,
            user=self.user
        )
        
    def test_start_at_auto_populated(self):
        """Test start_at is automatically set"""
        duty = DutyStatus.objects.create(
            status="ON_DUTY",
            location="95 St. Andre Ave",
            driver=self.driver
        )
        self.assertIsNotNone(duty.start_at)
        self.assertAlmostEqual(
            timezone.now(),
            duty.start_at,
            delta=timezone.timedelta(seconds=1)
        )

    def test_end_at_null_by_default(self):
        """Test end_at is nullable"""
        duty = DutyStatus.objects.create(
            status="ON_DUTY",
            location="967 South Bound",
            driver=self.driver
        )
        self.assertIsNone(duty.end_at)

    def test_duration_property(self):
        """Test duration calculation"""
        duty = DutyStatus.objects.create(
            status="ON_DUTY",
            location="1082 Martyris Ave",
            driver=self.driver
        )
        self.assertIsNone(duty.duration)  # No end_at set
        
        duty.end_at = duty.start_at + timezone.timedelta(hours=2)
        duty.save()
        self.assertEqual(duty.duration.total_seconds(), 7200)  # 2 hours

    def test_invalid_time_range(self):
        """Test end_at cannot be before start_at"""
        duty = DutyStatus.objects.create(
            status="ON_DUTY",
            location="Old Traford Street",
            driver=self.driver
        )
        duty.end_at = duty.start_at - timezone.timedelta(hours=1)
        
        with self.assertRaises(ValidationError):
            duty.full_clean()
            
class BaseModelTest(TestCase):
    def setUp(self):
        # Create a concrete model instance to test BaseModel
        self.carrier = Carrier.objects.create(
            name="DHL",
            address="409 St. Petersburg, Boulevard"
        )

    def test_uuid_primary_key(self):
        """Test that the primary key is a UUID"""
        self.assertIsInstance(self.carrier.id, uuid.UUID)
        self.assertEqual(len(str(self.carrier.id)), 36)

    def test_created_at_auto_populated(self):
        """Test created_at is automatically set"""
        self.assertIsNotNone(self.carrier.created_at)

    def test_updated_at_auto_populated(self):
        """Test updated_at is automatically set"""
        self.assertIsNotNone(self.carrier.updated_at)

    def test_str_representation(self):
        """Test string representation"""
        expected_str = f"[Carrier] ({self.carrier.id})"
        self.assertIn(expected_str, str(self.carrier))

    def test_to_dict_method(self):
        """Test dictionary conversion"""
        data = self.carrier.to_dict()
        self.assertEqual(str(self.carrier.id), data['id'])
        self.assertEqual("Carrier", data['__class__'])
        self.assertEqual(self.carrier.name, data['name'])
        self.assertEqual(self.carrier.address, data['address'])

    def test_ordering_meta(self):
        """Test default ordering"""
        Carrier.objects.create(name="Mega Trash", address="456 Gordon Ave")
        carriers = Carrier.objects.all()
        self.assertGreater(
            carriers[1].created_at,
            carriers[0].created_at
        )