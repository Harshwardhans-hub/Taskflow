# Taskflow Security Baseline

This document records deployment checks for maintainers. It does not change application settings.

## Configuration that must be externalized

- The current settings module contains a Django secret-key fallback and a database password in source code. Treat those values as exposed because the repository is public.
- Generate a new production `SECRET_KEY`, set it through the deployment environment, and remove the hard-coded fallback.
- Rotate the database password with the database provider, then supply it through a secret environment variable or a protected `DATABASE_URL`.
- Review the Git history for older credential values. A later code change does not remove values from earlier commits.
- Do not commit local `.env` files or database dumps.

## Deployment checks

- Replace wildcard `ALLOWED_HOSTS` with the exact deployed hostnames.
- Keep `DEBUG=False` in production.
- Use HTTPS and configure secure session and CSRF cookies at the deployment boundary.
- Restrict database access to the application service and use a least-privilege database account.
- Add tests for authenticated access and for cross-user object isolation on both HTML and API endpoints.

## Current regression coverage

The task ownership tests cover list, detail, update, and delete access boundaries. The API tests additionally cover authenticated list/detail/create/delete behavior. Run the project's Django test suite before deployment.

This document is guidance only; existing settings and runtime behavior are unchanged.
