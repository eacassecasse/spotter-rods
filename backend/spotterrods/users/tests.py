#!/usr/bin/python3

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.exceptions import ValidationError
from users.models import User

class UserModelTest(TestCase):
    def test_create_user(self):
        """Test basic user creation"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            name='Test User'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.name, 'Test User')
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        """Test superuser creation"""
        admin = User.objects.create_superuser(
            username='admin',
            password='adminpass',
            name='Admin'
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_username_required(self):
        """Username is required"""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username='',
                password='testpass123'
            )

    def test_role_validation(self):
        """Test role validation"""
        user = User(
            username='testuser',
            password='testpass123',
            name='Test User',
            role='invalid_role'
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

class UserAPITests(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'name': 'Test User',
            'role': 'driver'
        }

    def test_user_registration(self):
        """Test user registration"""
        response = self.client.post(
            reverse('user-registration'),
            self.user_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.role, 'driver')

    def test_user_login(self):
        """Test user login"""
        User.objects.create_user(
            username='testuser',
            password='testpass123',
            name='Test User'
        )
        response = self.client.post(
            reverse('user-authentication'),
            {
                'username': 'testuser',
                'password': 'testpass123'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)

    def test_password_validation(self):
        """Test password validation rules"""
        weak_password_data = {
            **self.user_data,
            'password': '123'  # Too short
        }
        response = self.client.post(
            reverse('user-registration'),
            weak_password_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)