from datetime import datetime
import re

VALID_ROLES = {"admin", "manager", "developer"}
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

class User:
    def __init__(self, username, email, role) -> None:
        username = str(username).strip()
        email = str(email).strip()
        role = str(role).strip()

        if not username:
            raise ValueError("username must not be empty")
        if role not in VALID_ROLES:
            raise ValueError(f"Invalid role: {role}")
        if not self._is_valid_email(email):
            raise ValueError(f"Invalid email: {email}")

        self.id = None
        self.username = username
        self.email = email
        self.role = role
        self.registration_date = datetime.now()

    def _is_valid_email(self, email) -> bool:
        return bool(EMAIL_RE.match(str(email).strip()))

    def update_info(self, username=None, email=None, role=None) -> None:
        if username is not None:
            username = str(username).strip()
            if not username:
                raise ValueError("username must not be empty")
            self.username = username

        if email is not None:
            email = str(email).strip()
            if not self._is_valid_email(email):
                raise ValueError(f"Invalid email: {email}")
            self.email = email

        if role is not None:
            role = str(role).strip()
            if role not in VALID_ROLES:
                raise ValueError(f"Invalid role: {role}")
            self.role = role


    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "registration_date": self.registration_date.isoformat(),
        }