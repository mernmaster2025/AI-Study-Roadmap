"""FastAPI application entrypoint."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.config import get_settings
from app.docs import API_DESCRIPTION, OPENAPI_TAGS, scalar_html
from app.routers import auth, content, execute, oauth, progress, quizzes

settings = get_settings()

app = FastAPI(
    title="AI Study Platform API",
    version="0.2.0",
    description=API_DESCRIPTION,
    openapi_tags=OPENAPI_TAGS,
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc",    # ReDoc
    contact={"name": "AI Study Platform", "url": settings.frontend_origin},
    license_info={"name": "MIT"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_origin_regex=settings.cors_origin_regex or None,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Authlib stores the OAuth "state" between login redirect and callback in a
# signed session cookie.
app.add_middleware(SessionMiddleware, secret_key=settings.jwt_secret)

app.include_router(auth.router)
app.include_router(oauth.router)
app.include_router(content.router)
app.include_router(execute.router)
app.include_router(quizzes.router)
app.include_router(progress.router)


@app.get("/scalar", include_in_schema=False)
def scalar_docs():
    """Scalar API reference — the primary, modern docs UI."""
    return scalar_html(app.openapi_url or "/openapi.json", app.title)


@app.get("/api/health", tags=["health"])
def health():
    """Liveness probe."""
    return {"status": "ok"}
