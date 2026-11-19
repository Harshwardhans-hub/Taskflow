"""Regression tests for the task creation and editing form."""

from django.test import SimpleTestCase

from .forms import TaskForm


class TaskFormTests(SimpleTestCase):
    def test_form_exposes_expected_task_fields(self):
        form = TaskForm()

        self.assertEqual(
            set(form.fields),
            {"title", "description", "status", "priority", "due_date"},
        )

    def test_form_widgets_keep_bootstrap_classes_and_date_input(self):
        form = TaskForm()

        for field_name in ("title", "description", "status", "priority", "due_date"):
            with self.subTest(field=field_name):
                self.assertIn("form-control", form.fields[field_name].widget.attrs["class"])

        self.assertEqual(form.fields["due_date"].widget.input_type, "date")
        self.assertEqual(form.fields["description"].widget.attrs["rows"], 4)

    def test_empty_title_is_invalid(self):
        form = TaskForm(data={
            "title": "",
            "description": "",
            "status": "todo",
            "priority": "medium",
            "due_date": "",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)


if __name__ == "__main__":
    import unittest
    unittest.main()
