"""Regression tests for per-user task visibility and access control."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskOwnershipTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="test-pass-123")
        self.other_user = User.objects.create_user(username="other", password="test-pass-123")
        self.owned_task = Task.objects.create(user=self.owner, title="Owner task")
        self.other_task = Task.objects.create(user=self.other_user, title="Private task")
        self.client.force_login(self.owner)

    def test_task_list_only_shows_signed_in_users_tasks(self):
        response = self.client.get(reverse("task-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Owner task")
        self.assertNotContains(response, "Private task")

    def test_owner_can_view_task_detail(self):
        response = self.client.get(reverse("task-detail", args=[self.owned_task.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Owner task")

    def test_another_user_cannot_view_task_detail(self):
        response = self.client.get(reverse("task-detail", args=[self.other_task.pk]))

        self.assertEqual(response.status_code, 404)

    def test_another_user_cannot_update_task(self):
        response = self.client.get(reverse("task-update", args=[self.other_task.pk]))

        self.assertEqual(response.status_code, 404)

    def test_another_user_cannot_delete_task(self):
        response = self.client.get(reverse("task-delete", args=[self.other_task.pk]))

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Task.objects.filter(pk=self.other_task.pk).exists())


class TaskModelTests(TestCase):
    def test_new_task_has_expected_defaults(self):
        user = User.objects.create_user(username="student", password="test-pass-123")
        task = Task.objects.create(user=user, title="Prepare project report")

        self.assertEqual(task.status, "todo")
        self.assertEqual(task.priority, "medium")
        self.assertEqual(str(task), "Prepare project report")
