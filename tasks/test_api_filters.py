"""Tests for optional search and filter parameters on the task list API."""

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Task


class TaskApiFilterTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="filter-user", password="test-pass-123")
        self.other_user = User.objects.create_user(username="filter-other", password="test-pass-123")
        Task.objects.create(
            user=self.user,
            title="Revise DBMS",
            description="Normalization and joins",
            status="todo",
            priority="high",
        )
        Task.objects.create(
            user=self.user,
            title="Practice Python",
            description="Graph traversal",
            status="in_progress",
            priority="medium",
        )
        Task.objects.create(
            user=self.other_user,
            title="Private DBMS task",
            description="Must not leak",
            status="todo",
            priority="high",
        )
        self.client.force_authenticate(user=self.user)

    def test_search_matches_title_or_description(self):
        response = self.client.get(reverse("task-list-api"), {"search": "graph"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["title"] for item in response.data], ["Practice Python"])

    def test_status_and_priority_filters_can_be_combined(self):
        response = self.client.get(
            reverse("task-list-api"),
            {"status": "todo", "priority": "high"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["title"] for item in response.data], ["Revise DBMS"])

    def test_filters_never_return_another_users_tasks(self):
        response = self.client.get(reverse("task-list-api"), {"search": "DBMS"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["title"] for item in response.data], ["Revise DBMS"])

    def test_invalid_status_or_priority_returns_bad_request(self):
        invalid_status = self.client.get(reverse("task-list-api"), {"status": "waiting"})
        invalid_priority = self.client.get(reverse("task-list-api"), {"priority": "urgent"})

        self.assertEqual(invalid_status.status_code, 400)
        self.assertEqual(invalid_priority.status_code, 400)


if __name__ == "__main__":
    unittest.main()
