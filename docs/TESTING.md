# TaskFlow testing guide

## Prerequisites

Use the Python version supported by the project and install its declared dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell, activate with `.venv\\Scripts\\Activate.ps1`.

## Run checks

Run Django's configuration checks and full test discovery from the repository root:

```bash
python manage.py check
python manage.py test --verbosity 2
```

The GitHub Actions workflow runs these same commands on pushes and pull requests targeting `main`.

## Test boundaries

- Form tests should use Django's lightweight test classes when no database access is needed.
- API tests should create separate users and verify that one account cannot read or mutate another account's tasks.
- Prefer isolated tests with controlled fixtures; do not depend on a deployed database or live third-party services.
- Never add production credentials or personal user data to test fixtures.
