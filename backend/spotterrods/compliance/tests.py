# tests/test_duty_status.py
from django.test import TestCase
from rest_framework.test import APIClient
from users.models import User, UserRoles
from .models import DutyStatus

class DutyStatusTests(TestCase):
    def setUp(self):
        self.driver = User.objects.create(
            username="driver1", 
            role=UserRoles.DRIVER
        )
        self.dispatcher = User.objects.create(
            username="dispatcher1",
            role=UserRoles.DISPATCHER
        )
        self.status = DutyStatus.objects.create(
            driver=self.driver,
            status="ON_DUTY",
            location="Test Location"
        )

    def test_driver_can_create_status(self):
        client = APIClient()
        client.force_authenticate(user=self.driver)
        response = client.post(
            "/api/v1/duty-status/",
            {"status": "DRIVING", "location": "New Location"},
            format="json"
        )
        self.assertEqual(response.status_code, 201)

    def test_dispatcher_cannot_modify_status(self):
        client = APIClient()
        client.force_authenticate(user=self.dispatcher)
        response = client.patch(
            f"/api/duty-status/{self.status.id}/",
            {"status": "OFF_DUTY"},
            format="json"
        )
        self.assertEqual(response.status_code, 403)

    def test_24_hour_edit_window(self):
        from django.utils import timezone
        from datetime import timedelta
        old_status = DutyStatus.objects.create(
            driver=self.driver,
            status="OFF_DUTY",
            start_at=timezone.now() - timedelta(hours=25)
        )
        client = APIClient()
        client.force_authenticate(user=self.driver)
        response = client.patch(
            f"/api/duty-status/{old_status.id}/",
            {"status": "ON_DUTY"},
            format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("24 hours", str(response.data))