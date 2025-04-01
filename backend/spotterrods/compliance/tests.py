#!/usr/bin/python3

from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError
from rest_framework import status
from fleet.models import Driver, Carrier
from compliance.models import DutyStatus, RestBreak
from users.models import User, UserRoles

class DutyStatusModelTest(APITestCase):
    def setUp(self):
        # Create carrier first
        self.carrier = Carrier.objects.create(name="Test Carrier")
        
        # Create user
        self.user = User.objects.create(
            username='testdriver',
            password='testpass',
            name='Test Driver',
            role=UserRoles.DRIVER
        )
        
        # Create driver profile linked to user
        self.driver = Driver.objects.create(
            user=self.user,
            name="Test Driver",
            license_number="DL12345678",
            carrier=self.carrier
        )
        
        # Now create duty status with driver instance
        self.status = DutyStatus.objects.create(
            status="ON_DUTY",
            location="Test Location",
            driver=self.driver,  # Pass the Driver instance, not User
            start_at=timezone.now() - timezone.timedelta(hours=2)
        )

    def test_status_transition_validation(self):
        """Test valid status transitions"""
        # Start with OFF_DUTY
        duty = DutyStatus.objects.create(
            status="OFF_DUTY",
            location="Home",
            driver=self.driver
        )
        
        # OFF_DUTY -> ON_DUTY is valid
        duty.status = "ON_DUTY"
        duty.full_clean()
        
        # ON_DUTY -> DRIVING is valid
        duty.status = "DRIVING"
        duty.full_clean()
        
        # DRIVING -> OFF_DUTY is invalid (must go through ON_DUTY)
        duty.status = "OFF_DUTY"
        with self.assertRaises(ValidationError):
            duty.full_clean()

class DutyStatusAPITests(APITestCase):
    def setUp(self):
        self.carrier = Carrier.objects.create(name="Test Carrier")
        self.driver_user = User.objects.create_user(
            username='driver',
            password='driverpass',
            name='Driver',
            role=UserRoles.DRIVER
        )
        self.driver = Driver.objects.create(
            user=self.driver_user,
            name="Test Driver",
            license_number="DL12345678",
            carrier=self.carrier
        )
        self.duty_data = {
            'status': 'ON_DUTY',
            'location': 'Test Location'
        }

    def test_create_duty_status_as_driver(self):
        """Driver should create their own duty status"""
        self.client.force_authenticate(user=self.driver_user)
        response = self.client.post(
            reverse('duty-status-list', kwargs={'driver_id': self.driver.id}),
            self.duty_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DutyStatus.objects.count(), 1)
        duty = DutyStatus.objects.first()
        self.assertEqual(duty.status, 'ON_DUTY')
        self.assertEqual(duty.driver, self.driver)

    def test_cannot_modify_old_status(self):
        """Cannot modify status older than 24 hours"""
        old_duty = DutyStatus.objects.create(
            status="ON_DUTY",
            location="Old Location",
            driver=self.driver,
            start_at=timezone.now() - timezone.timedelta(days=2)
        )
        
        self.client.force_authenticate(user=self.driver_user)
        response = self.client.patch(
            reverse('duty-status-details', args=[old_duty.id], kwargs={'driver_id': self.driver.id}),
            {'status': 'OFF_DUTY'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'FMCSA violation')
        
class RestBreakTest(APITestCase):
    def setUp(self):
        self.carrier = Carrier.objects.create(name="Test Carrier")
        self.driver_user = User.objects.create_user(
            username='driver',
            password='driverpass',
            name='Driver',
            role=UserRoles.DRIVER
        )
        self.driver = Driver.objects.create(
            user=self.driver_user,
            name="Test Driver",
            license_number="DL12345678",
            carrier=self.carrier
        )
        
        # Start duty status
        self.duty = DutyStatus.objects.create(
            status="ON_DUTY",
            location="Test Location",
            driver=self.driver
        )

    def test_create_rest_break(self):
        """Driver should create rest breaks"""
        self.client.force_authenticate(user=self.driver_user)
        response = self.client.post(
            reverse('rest-break-list', kwargs={'driver_id': self.driver.id}),
            {'type': 'OFF_DUTY'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RestBreak.objects.count(), 1)
        rest_break = RestBreak.objects.first()
        self.assertEqual(rest_break.type, 'OFF_DUTY')
        self.assertEqual(rest_break.driver, self.driver)

    def test_break_duration_calculation(self):
        """Test break duration calculation"""
        rest_break = RestBreak.objects.create(
            type="OFF_DUTY",
            driver=self.driver
        )
        self.assertIsNone(rest_break.duration)  # No end_at
        
        rest_break.end_at = rest_break.start_at + timezone.timedelta(minutes=30)
        rest_break.save()
        self.assertEqual(rest_break.duration.total_seconds(), 1800)