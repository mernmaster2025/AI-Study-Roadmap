"""Rich OpenAPI metadata + the Scalar API reference UI.

Scalar (https://scalar.com) is a modern replacement for Swagger UI: a cleaner
three-pane reference with a built-in request playground. It renders our existing
OpenAPI schema, so it stays in sync automatically.
"""
from fastapi.responses import HTMLResponse

API_DESCRIPTION = """
Backend for the **AI Study Platform** — a 12-phase, hands-on AI curriculum.

### What you can do here
- **Auth** — `dev-login` for a passwordless demo token, or GitHub/Google OAuth.
- **Content** — browse phases → lessons → challenges.
- **Execute** — run + grade Python submissions against hidden test cases.
- **Quizzes** — fetch a lesson quiz and submit answers for instant grading.
- **Progress** — per-phase completion, challenges solved, quizzes passed.

### Authentication
Most write endpoints need a bearer token. Grab one from
`POST /api/auth/dev-login`, then click **Authorize** (Swagger) or set the
`Authorization: Bearer <token>` header (Scalar) to try protected routes.

Docs UIs: **Scalar** at `/scalar` · Swagger at `/docs` · ReDoc at `/redoc`.
"""

# Ordered tag descriptions — controls grouping/order in every docs UI.
OPENAPI_TAGS = [
    {"name": "auth", "description": "Dev-login and the current-user endpoint."},
    {"name": "oauth", "description": "GitHub/Google OAuth login, callback, and provider status."},
    {"name": "content", "description": "Phases, lessons, and challenges (read-only)."},
    {"name": "execute", "description": "Run and grade a challenge submission."},
    {"name": "quizzes", "description": "Fetch a lesson quiz and submit answers."},
    {"name": "progress", "description": "Per-user progress overview."},
    {"name": "health", "description": "Liveness probe."},
]

# Pin a Scalar version for reproducible rendering. Bump intentionally.
_SCALAR_CDN = "https://cdn.jsdelivr.net/npm/@scalar/api-reference@1.32.10"


def scalar_html(openapi_url: str, title: str) -> HTMLResponse:
    """Standalone Scalar reference page pointed at our OpenAPI schema."""
    html = f"""<!doctype html>
<html>
  <head>
    <title>{title} — API Reference</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📚</text></svg>" />
    <style>body {{ margin: 0; }}</style>
  </head>
  <body>
    <script
      id="api-reference"
      data-url="{openapi_url}"
      data-configuration='{{"theme":"purple","layout":"modern","hideDownloadButton":false}}'></script>
    <script src="{_SCALAR_CDN}"></script>
  </body>
</html>"""
    return HTMLResponse(html)
