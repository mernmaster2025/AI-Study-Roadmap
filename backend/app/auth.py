"""Minimal JWT auth.

For the vertical slice we ship a `dev-login` that mints a token for a demo user
so the whole flow runs without OAuth keys. The production path (GitHub/Google via
NextAuth) issues the same shape of JWT — swap the token minting for the OAuth
callback and the rest of the backend is unchanged.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models import User

settings = get_settings()
_bearer = HTTPBearer(auto_error=True)


def create_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    db: Session = Depends(get_db),
) -> User:
    creds_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
        user_id = payload.get("sub")
    except JWTError:
        raise creds_exc

    if not user_id:
        raise creds_exc
    user = db.get(User, user_id)
    if user is None:
        raise creds_exc
    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Dependency that allows only admin users (403 otherwise)."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )
    return current_user
