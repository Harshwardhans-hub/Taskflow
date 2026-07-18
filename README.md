#  TaskFlow

A full-stack task management web application built with Django.

**Live Demo:** https://taskflow-hlya.onrender.com

---

##  Features

- 🔐 **User Authentication** — Register, Login, Logout
- ✅ **Full CRUD** — Create, Read, Update, Delete tasks
- 🔒 **Data Isolation** — Every user sees only their own tasks
- 🔍 **Search & Filter** — Search by title/description, filter by status
- 📄 **Pagination** — 10 tasks per page with preserved search state
- 💬 **Flash Messages** — Feedback on every action
- 📡 **REST API** — JSON API endpoints via Django REST Framework
- 📊 **Dashboard** — Task statistics on the home page

---

##  Tech Stack

| Layer          | →  | Technology                  |
|----------------|----|-----------------------------|
| Backend        | →  | Django 6.0                  |
| API            | →  | Django REST Framework        |
| Frontend       | →  | Bootstrap 5                 |
| Database       | →  | MySQL *(local)*              |
| Database       | →  | PostgreSQL *(production)*    |
| Web Server     | →  | Gunicorn                    |
| Static Files   | →  | WhiteNoise                  |
| Deployment     | →  | Render                      |

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/tasks/` | List all tasks for logged-in user |
| POST | `/api/tasks/` | Create a new task |
| GET | `/api/tasks/<id>/` | Get a single task |
| PUT | `/api/tasks/<id>/` | Update a task |
| DELETE | `/api/tasks/<id>/` | Delete a task |

---

##  Run Locally

```bash
# Clone the repo
git clone https://github.com/Harshwardhans-hub/Taskflow.git
cd Taskflow

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up MySQL database and update settings.py
# then run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

---

## 📁 Project Structure

```
taskflow/           ← Django project settings & URLs
tasks/              ← Main app (models, views, forms, API)
  models.py         ← Task model with ForeignKey to User
  views.py          ← All views with @login_required
  serializers.py    ← DRF Serializer for Task model
  api_views.py      ← REST API views (TaskListAPI, TaskDetailAPI)
  urls.py           ← App-level URL routing
templates/          ← HTML templates (base, home, tasks)
static/             ← CSS and static assets
build.sh            ← Render build script
requirements.txt    ← Python dependencies
```

---

## 👨‍Author

**Harshwardhan Sharma**
