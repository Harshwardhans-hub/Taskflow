"""Tests for the task creation and editing form's field constraints."""

from django.test import SimpleTestCase

from .forms import TaskForm


class TaskFormValidationTests(SimpleTestCase):
    def test_valid_task_data_is_accepted(self):
        form = TaskForm(data={
            "title": "Prepare DBMS notes",
            "description": "Revise normalization",
            "status": "todo",
            "priority": "high",
            "due_date": "2026-12-01",
        })

        self.assertTrue(form.is_valid(), form.errors)

    def test_title_longer_than_model_limit_is_rejected(self):
        form = TaskForm(data={
            "title": "x" * 201,
            "description": "",
            "status": "todo",
            "priority": "medium",
            "due_date": "",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_unknown_status_and_priority_are_rejected(self):
        form = TaskForm(data={
            "title": "Invalid choices",
            "description": "",
            "status": "waiting",
            "priority": "urgent",
            "due_date": "",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("status", form.errors)
        self.assertIn("priority", form.errors)
