#!/usr/bin/python3

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.exceptions import ValidationError
from fleet.models import Carrier, Driver
from compliance.models import DutyStatus
from shipping.models import Shipping
from users.models import User

class ShippingModelTest(TestCase):
    def setUp(self):
        self.carrier = Carrier.objects.create(name="Test Carrier")

    def test_create_shipping(self):
        """Test basic shipping creation"""
        shipping = Shipping.objects.create(
            number="SHIP123",
            commodity="Test Commodity",
            carrier=self.carrier
        )
        self.assertEqual(shipping.number, "SHIP123")
        self.assertEqual(shipping.commodity, "Test Commodity")
        self.assertEqual(shipping.carrier, self.carrier)

    def test_number_format_validation(self):
        """Test shipping number format"""
        # Valid format
        Shipping.objects.create(
            number="ABCD1234",
            commodity="Test",
            carrier=self.carrier
        )
        
        # Invalid format (too long)
        shipping = Shipping(
            number="INVALIDNUMBER12345",  # > 14 chars
            commodity="Test",
            carrier=self.carrier
        )
        with self.assertRaises(ValidationError):
            shipping.full_clean()
            
class ShippingAPITests(APITestCase):
    def setUp(self):
        self.carrier = Carrier.objects.create(name="Test Carrier")
        self.dispatcher = User.objects.create_user(
            username='dispatcher',
            password='dispatcherpass',
            name='Dispatcher',
            role='dispatcher'
        )
        self.driver_user = User.objects.create_user(
            username='driver',
            password='driverpass',
            name='Driver',
            role='driver'
        )
        self.driver = Driver.objects.create(
            user=self.driver_user,
            name="Test Driver",
            license_number="DL12345678",
            carrier=self.carrier
        )
        self.shipping_data = {
            'number': 'SHIP123',
            'commodity': 'Test Commodity',
            'carrier': self.carrier.id
        }

    def test_create_shipping_as_dispatcher(self):
        """Dispatcher should create shipments"""
        self.client.force_authenticate(user=self.dispatcher)
        response = self.client.post(
            reverse('carrier-shippings', kwargs={'carrier_id': self.carrier.id}),
            self.shipping_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Shipping.objects.count(), 1)
        shipping = Shipping.objects.first()
        self.assertEqual(shipping.number, 'SHIP123')

    def test_cannot_assign_to_off_duty_driver(self):
        """Cannot assign shipment to off-duty driver"""
        # Create shipping with driver assignment
        shipping_data = {
            **self.shipping_data,
            'driver': self.driver.id
        }
        
        self.client.force_authenticate(user=self.dispatcher)
        response = self.client.post(
            reverse('carrier-shippings', kwargs={'carrier_id': self.carrier.id}),
            shipping_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Set driver to ON_DUTY and try again
        DutyStatus.objects.create(
            status="ON_DUTY",
            location="Test Location",
            driver=self.driver
        )
        response = self.client.post(
            reverse('carrier-shippings', kwargs={'carrier_id': self.carrier.id}),
            shipping_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
