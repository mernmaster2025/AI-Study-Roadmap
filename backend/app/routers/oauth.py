"""OAuth login/callback for GitHub and Google (Authlib).

Flow:
  GET /api/auth/login/{provider}      -> redirect to the provider
  GET /api/auth/callback/{provider}   -> exchange code, upsert user, mint our
                                         JWT, redirect to the frontend with
                                         ?token=... (the SPA stores it).

If a provider isn't configured, the login endpoint returns 503 and dev-login
remains available.
"""
from urllib.parse import urlencode

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select

from app.auth import create_access_token
from app.config import get_settings
from app.database import SessionLocal
from app.models import User
from app.oauth import oauth

router = APIRouter(prefix="/api/auth", tags=["oauth"])
settings = get_settings()

_ENABLED = {"github": lambda: settings.github_enabled, "google": lambda: settings.google_enabled}


@router.get("/providers")
def providers():
    """Which OAuth providers are configured — the frontend shows only these."""
    return {"github": settings.github_enabled, "google": settings.google_enabled}


def _require_provider(provider: str):
    if provider not in _ENABLED:
        raise HTTPException(status_code=404, detail="Unknown provider")
    if not _ENABLED[provider]():
        raise HTTPException(
            status_code=503,
            detail=(
                f"{provider} OAuth is not configured. Set "
                f"{provider.upper()}_CLIENT_ID / _SECRET in the backend .env."
            ),
        )


def _upsert_user(email: str, name: str, avatar_url: str | None) -> str:
    """Find or create a user by email; return a signed backend JWT."""
    db = SessionLocal()
    try:
        user = db.scalar(select(User).where(User.email == email))
        if user is None:
            user = User(email=email, name=name or email, avatar_url=avatar_url)
            db.add(user)
            db.commit()
            db.refresh(user)
        elif avatar_url and not user.avatar_url:
            user.avatar_url = avatar_url
            db.commit()
        return create_access_token(user.id)
    finally:
        db.close()


@router.get("/login/{provider}")
async def login(provider: str, request: Request):
    _require_provider(provider)
    redirect_uri = str(request.url_for("oauth_callback", provider=provider))
    return await oauth.create_client(provider).authorize_redirect(request, redirect_uri)


@router.get("/callback/{provider}", name="oauth_callback")
async def oauth_callback(provider: str, request: Request):
    _require_provider(provider)
    client = oauth.create_client(provider)

    try:
        token = await client.authorize_access_token(request)
    except Exception as exc:  # noqa: BLE001 - surface auth failures to the SPA
        return _redirect_with_error(str(exc))

    if provider == "google":
        info = token.get("userinfo") or await client.userinfo(token=token)
        email = info.get("email")
        name = info.get("name") or email
        avatar = info.get("picture")
    else:  # github
        profile = (await client.get("user", token=token)).json()
        email = profile.get("email")
        if not email:  # email may be private — fetch the verified primary
            emails = (await client.get("user/emails", token=token)).json()
            primary = next(
                (e for e in emails if e.get("primary") and e.get("verified")),
                next(iter(emails), None),
            )
            email = primary.get("email") if primary else None
        name = profile.get("name") or profile.get("login") or email
        avatar = profile.get("avatar_url")

    if not email:
        return _redirect_with_error("Could not read an email from the provider")

    jwt_token = _upsert_user(email, name, avatar)
    target = f"{settings.frontend_origin}{settings.oauth_success_path}?{urlencode({'token': jwt_token})}"
    return RedirectResponse(url=target)


def _redirect_with_error(message: str) -> RedirectResponse:
    target = (
        f"{settings.frontend_origin}{settings.oauth_success_path}"
        f"?{urlencode({'error': message})}"
    )
    return RedirectResponse(url=target)
