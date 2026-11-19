"""Tests for due-date range and ordering query parameters."""

from datetime import date
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Task


class TaskApiDateFilterTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="date-filter-user", password="test-pass-123")
        Task.objects.create(user=self.user, title="Later task", due_date=date(2026, 12, 10))
        Task.objects.create(user=self.user, title="Earlier task", due_date=date(2026, 11, 25))
        Task.objects.create(user=self.user, title="No due date")
        self.client.force_authenticate(user=self.user)

    def test_due_after_and_before_filters(self):
        response = self.client.get(
            reverse("task-list-api"),
            {"due_after": "2026-12-01", "due_before": "2026-12-31"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["title"] for item in response.data], ["Later task"])

    def test_invalid_date_filter_returns_bad_request(self):
        response = self.client.get(reverse("task-list-api"), {"due_after": "tomorrow"})

        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.data)

    def test_ordering_uses_allow_list(self):
        response = self.client.get(reverse("task-list-api"), {"ordering": "title"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [item["title"] for item in response.data],
            ["Earlier task", "Later task", "No due date"],
        )

    def test_unknown_ordering_field_is_rejected(self):
        response = self.client.get(reverse("task-list-api"), {"ordering": "user__password"})

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
