"""Promote a user to admin (or create one) for the admin panel.

Usage:
    python make_admin.py <email> [name] [password]

- If the user exists, they are granted admin.
- If not, a new admin account is created. Provide a password to enable
  email/password login; otherwise the account has no password (log in via
  dev-login or OAuth with that email).

Examples:
    python make_admin.py me@example.com
    python make_admin.py admin@example.com "Site Admin" "s3cret-pass"
"""
import sys

from sqlalchemy import select

from app.database import SessionLocal
from app.models import User
from app.security import hash_password


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python make_admin.py <email> [name] [password]")
    email = sys.argv[1].lower()
    name = sys.argv[2] if len(sys.argv) > 2 else "Admin"
    password = sys.argv[3] if len(sys.argv) > 3 else None

    db = SessionLocal()
    try:
        user = db.scalar(select(User).where(User.email == email))
        if user is None:
            user = User(
                email=email,
                name=name,
                is_admin=True,
                password_hash=hash_password(password) if password else None,
            )
            db.add(user)
            action = "Created admin"
        else:
            user.is_admin = True
            if password:
                user.password_hash = hash_password(password)
            action = "Promoted to admin"
        db.commit()
        db.refresh(user)
        print(f"{action}: {user.email} (id={user.id})")
        if password:
            print("  Password set — you can log into the admin panel with it.")
        elif user.password_hash is None:
            print("  No password — set one by re-running with a password argument.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
