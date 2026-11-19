"""Lightweight tests for Task model defaults and representation."""

from django.test import SimpleTestCase

from .models import Task


class TaskModelTests(SimpleTestCase):
    def test_new_task_uses_expected_workflow_defaults(self):
        task = Task(title="Prepare project report")

        self.assertEqual(task.status, "todo")
        self.assertEqual(task.priority, "medium")
        self.assertIsNone(task.due_date)

    def test_task_string_representation_uses_title(self):
        task = Task(title="Revise database notes")

        self.assertEqual(str(task), "Revise database notes")

    def test_status_and_priority_choices_are_explicit(self):
        self.assertEqual(
            {value for value, _label in Task.STATUS_CHOICES},
            {"todo", "in_progress", "done"},
        )
        self.assertEqual(
            {value for value, _label in Task.PRIORITY_CHOICES},
            {"low", "medium", "high"},
        )


if __name__ == "__main__":
    import unittest
    unittest.main()
