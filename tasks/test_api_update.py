"""Regression tests for task API updates."""

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Task


class TaskApiUpdateTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="update-owner", password="test-pass-123")
        self.other_user = User.objects.create_user(username="update-other", password="test-pass-123")
        self.own_task = Task.objects.create(user=self.owner, title="Original title")
        self.private_task = Task.objects.create(user=self.other_user, title="Private original")
        self.client.force_authenticate(user=self.owner)

    def test_owner_can_update_task(self):
        response = self.client.put(
            reverse("task-detail-api", args=[self.own_task.pk]),
            {"title": "Updated title", "description": "Updated through API", "status": "in_progress",
             "priority": "high", "due_date": None},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.own_task.refresh_from_db()
        self.assertEqual(self.own_task.title, "Updated title")
        self.assertEqual(self.own_task.user, self.owner)

    def test_user_cannot_update_another_users_task(self):
        response = self.client.put(
            reverse("task-detail-api", args=[self.private_task.pk]),
            {"title": "Attempted takeover", "description": "", "status": "todo",
             "priority": "medium", "due_date": None},
            format="json",
        )

        self.assertEqual(response.status_code, 404)
        self.private_task.refresh_from_db()
        self.assertEqual(self.private_task.title, "Private original")
        self.assertEqual(self.private_task.user, self.other_user)

    def test_invalid_status_does_not_update_task(self):
        response = self.client.put(
            reverse("task-detail-api", args=[self.own_task.pk]),
            {"title": "Should not save", "description": "", "status": "unknown",
             "priority": "medium", "due_date": None},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.own_task.refresh_from_db()
        self.assertEqual(self.own_task.title, "Original title")
