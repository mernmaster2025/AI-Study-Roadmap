"""Auth routes. Dev-login for the slice; OAuth callbacks slot in here later."""
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import create_access_token, get_current_user
from app.database import get_db
from app.models import User
from app.schemas import DevLoginRequest, TokenResponse, UserOut

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/dev-login", response_model=TokenResponse)
def dev_login(payload: DevLoginRequest, db: Session = Depends(get_db)):
    """Log in (or lazily create) a user by email — no password.

    Stand-in for GitHub/Google OAuth so the slice is runnable out of the box.
    """
    user = db.scalar(select(User).where(User.email == payload.email))
    if user is None:
        user = User(email=payload.email, name=payload.name)
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_access_token(user.id)
    return TokenResponse(access_token=token, user=UserOut.model_validate(user))


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user
