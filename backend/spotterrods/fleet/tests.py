#!/usr/bin/python3

import re
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.exceptions import ValidationError
from fleet.models import Carrier, Driver, Truck, Trailer
from users.models import User, UserRoles

class CarrierModelTest(TestCase):
    def test_create_carrier(self):
        """Test basic carrier creation"""
        carrier = Carrier.objects.create(
            name="Expresso",
            address="123 Main St"
        )
        self.assertEqual(carrier.name, "Expresso")
        self.assertEqual(carrier.drivers.count(), 0)

    def test_string_representation(self):
        """Test carrier string representation"""
        carrier = Carrier.objects.create(name="Expresso")
        self.assertEqual(str(carrier), f"[Carrier] ({carrier.id}) {carrier.__dict__}")

class DriverModelTest(TestCase):
    def setUp(self):
        self.carrier = Carrier.objects.create(name="Test Carrier")

    def test_create_driver(self):
        """Test basic driver creation"""
        driver = Driver.objects.create(
            name="Albert Manfred",
            license_number="DL87654321",
            total_mileage_driven=1000.5,
            mileage_week=250.25,
            is_cdl_holder=True,
            carrier=self.carrier
        )
        self.assertEqual(driver.name, "Albert Manfred")
        self.assertEqual(driver.license_number, "DL87654321")
        self.assertTrue(driver.is_cdl_holder)

    def test_license_number_validation(self):
        """Test license number format validation"""
        driver = Driver(
            name="Test Driver",
            license_number="INVALID!",
            total_mileage_driven=0,
            carrier=self.carrier
        )
        with self.assertRaises(ValidationError):
            driver.full_clean()

    def test_mileage_validation(self):
        """Test mileage cannot be negative"""
        driver = Driver(
            name="Test Driver",
            license_number="DL12345678",
            total_mileage_driven=-100,
            carrier=self.carrier
        )
        with self.assertRaises(ValidationError):
            driver.full_clean()

class TruckModelTest(TestCase):
    def setUp(self):
        self.carrier = Carrier.objects.create(name="Test Carrier")

    def test_create_truck(self):
        """Test basic truck creation"""
        truck = Truck.objects.create(
            brand="Volvo",
            number="TRUCK123",
            current_mileage=10000,
            carrier=self.carrier
        )
        self.assertEqual(truck.brand, "Volvo")
        self.assertEqual(truck.number, "TRUCK123")
        self.assertEqual(truck.current_mileage, 10000)

    def test_mileage_validation(self):
        """Test mileage cannot be negative"""
        truck = Truck(
            brand="Volvo",
            number="TRUCK123",
            current_mileage=-100,
            carrier=self.carrier
        )
        with self.assertRaises(ValidationError):
            truck.full_clean()
            

class CarrierAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin',
            password='adminpass',
            name='Admin',
            role=UserRoles.ADMIN
        )
        self.carrier_data = {
            'name': 'Test Carrier',
            'address': '123 Test St'
        }

    def test_create_carrier_as_admin(self):
        """Admin should be able to create carriers"""
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            reverse('carrier-list'),
            self.carrier_data,
            format='json'
        )
        print(f"RESPONSE => {response.json()}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Carrier.objects.count(), 1)
        self.assertEqual(Carrier.objects.get().name, 'Test Carrier')

    def test_list_carriers(self):
        """Any authenticated user should list carriers"""
        Carrier.objects.create(name="Carrier 1")
        Carrier.objects.create(name="Carrier 2")
        
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('carrier-list'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

class DriverAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin',
            password='adminpass',
            name='Admin',
            role=UserRoles.ADMIN
        )
        self.carrier = Carrier.objects.create(name="Test Carrier")
        self.driver_data = {
            'name': 'Test Driver',
            'license_number': 'DL12345678',
            'total_mileage_driven': 1000,
            'mileage_week': 250,
            'is_cdl_holder': True,
            'carrier': self.carrier.id
        }

    def test_create_driver(self):
        """Admin should create drivers"""
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            reverse('driver-list', kwargs={'carrier_id': self.carrier.id}),
            self.driver_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Driver.objects.count(), 1)
        driver = Driver.objects.first()
        self.assertEqual(driver.name, 'Test Driver')
        self.assertEqual(driver.license_number, 'DL12345678')

    def test_driver_filtering(self):
        """Test filtering drivers by name"""
        Driver.objects.create(
            name="John Doe",
            license_number="DL11111111",
            carrier=self.carrier
        )
        Driver.objects.create(
            name="Jane Smith",
            license_number="DL22222222",
            carrier=self.carrier
        )
        
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(
            reverse('driver-list') + '?name=John'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'John Doe')