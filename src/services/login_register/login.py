import hashlib

from core.models import User

import streamlit as st


class LoginService:
    """Service for handling user login"""

    def __init__(self, user_repository=None):
        self.user_repository = user_repository

    def login_user(self, email: str, password: str) -> User | None:
        if self.user_repository:
            try:
                print(
                    f"=====================\nsearching for: {email}\n==========================\n"
                )
                user = self.user_repository.get_user_by_email(email)
                print(
                    f"=====================\nfound: {user.first_name}\n==========================\n"
                )
                if user and self._verify_password(password, user.password_hash):
                    return user
            except Exception as e:
                print(f"LoginService error: {e}")
                return None

    def _verify_password(self, password: str, stored_hash: str) -> bool:
        """Verify password against stored hash"""
        try:
            salt, hash_hex = stored_hash.split("$", 1)
            password_hash = hashlib.pbkdf2_hmac(
                "sha256", password.encode(), salt.encode(), 100000
            )
            return password_hash.hex() == hash_hex
        except ValueError:
            return False
