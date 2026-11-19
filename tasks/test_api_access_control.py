"""API regression tests for per-user Taskflow data isolation."""

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Task


class TaskApiOwnershipTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="api-owner", password="test-pass-123")
        self.other_user = User.objects.create_user(username="api-other", password="test-pass-123")
        self.own_task = Task.objects.create(user=self.owner, title="My API task")
        self.private_task = Task.objects.create(user=self.other_user, title="Another user's task")
        self.client.force_authenticate(user=self.owner)

    def test_api_list_returns_only_authenticated_users_tasks(self):
        response = self.client.get(reverse("task-list-api"))

        self.assertEqual(response.status_code, 200)
        titles = [item["title"] for item in response.data]
        self.assertIn("My API task", titles)
        self.assertNotIn("Another user's task", titles)

    def test_api_detail_allows_owner(self):
        response = self.client.get(reverse("task-detail-api", args=[self.own_task.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "My API task")

    def test_api_detail_hides_another_users_task(self):
        response = self.client.get(reverse("task-detail-api", args=[self.private_task.pk]))

        self.assertEqual(response.status_code, 404)

    def test_api_create_assigns_task_to_authenticated_user(self):
        response = self.client.post(
            reverse("task-list-api"),
            {"title": "Created through API", "description": "Ownership is server assigned"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        created = Task.objects.get(title="Created through API")
        self.assertEqual(created.user, self.owner)

    def test_api_delete_cannot_remove_another_users_task(self):
        response = self.client.delete(reverse("task-detail-api", args=[self.private_task.pk]))

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Task.objects.filter(pk=self.private_task.pk).exists())
