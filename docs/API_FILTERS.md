# Task List API Query Parameters

The authenticated `GET /api/tasks/` endpoint continues to return the signed-in user's tasks when no query parameters are supplied.

Optional query parameters:

| Parameter | Example | Behavior |
| --- | --- | --- |
| `search` | `?search=report` | Case-insensitive match in title or description |
| `status` | `?status=in_progress` | Filter by a declared task status |
| `priority` | `?priority=high` | Filter by a declared priority |
| `due_after` | `?due_after=2026-11-20` | Include tasks due on or after the date |
| `due_before` | `?due_before=2026-12-31` | Include tasks due on or before the date |
| `ordering` | `?ordering=-due_date` | Order by an allow-listed field |

Date values must use `YYYY-MM-DD`. Invalid filters return HTTP 400. Ordering accepts only `title`, `due_date`, `created_at`, and `priority`, optionally prefixed with `-` for descending order.

All filters are applied after restricting the queryset to the authenticated user. Query parameters cannot broaden access to another user's tasks.
