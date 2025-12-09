from typing import Dict, Any, Optional

from datetime import datetime
import hashlib
import secrets
import re
from dataclasses import dataclass

from core.models import User
from core.utils import hash_password


@dataclass
class UserRegistrationRequest:
    """Data class for user registration request"""

    email: str
    password: str
    first_name: str
    last_name: str


@dataclass
class UserRegistrationResponse:
    """Data class for user registration response"""

    success: bool
    user_id: Optional[str] = None
    message: str = ""
    errors: Optional[Dict[str, str]] = None


class RegistrationService:
    """Service for handling user registration"""

    def __init__(self, user_repository=None, email_service=None):
        self.user_repository = user_repository
        self.email_service = email_service

    def register_user(
        self, request: UserRegistrationRequest
    ) -> UserRegistrationResponse:
        """
        Register a new user

        Args:
            request: UserRegistrationRequest containing user details

        Returns:
            UserRegistrationResponse with registration result
        """
        try:
            validation_errors = self._validate_registration_data(request)
            if validation_errors:
                return UserRegistrationResponse(
                    success=False, message="Validation failed", errors=validation_errors
                )

            if self.user_repository and self.user_repository.get_user_by_email(
                request.email
            ):
                return UserRegistrationResponse(
                    success=False, message="User already exists with this email"
                )

            password_hash = hash_password(request.password)

            user_data = User(
                email=request.email.lower(),
                password_hash=password_hash,
                first_name=request.first_name,
                last_name=request.last_name,
                created_at=datetime.utcnow(),
                is_active=True,
                email_verified=False,
            )

            if self.user_repository:
                user = self.user_repository.register_user(user_data)

                # if self.email_service:
                #     self._send_verification_email(request.email, user_id)

                return UserRegistrationResponse(
                    success=True,
                    user_id=user.id,
                    message="User registered successfully",
                )
            else:
                return UserRegistrationResponse(
                    success=False, message="User repository not configured"
                )

        except Exception as e:
            return UserRegistrationResponse(
                success=False, message=f"Registration failed: {str(e)}"
            )

    def _validate_registration_data(
        self, request: UserRegistrationRequest
    ) -> Optional[Dict[str, str]]:
        """Validate registration data"""
        errors = {}

        if not request.email:
            errors["email"] = "Email is required"
        elif not self._is_valid_email(request.email):
            errors["email"] = "Invalid email format"

        if not request.password:
            errors["password"] = "Password is required"
        elif len(request.password) < 8:
            errors["password"] = "Password must be at least 8 characters long"
        elif not self._is_strong_password(request.password):
            errors["password"] = (
                "Password must contain uppercase, lowercase, number and special character"
            )

        if not request.first_name:
            errors["first_name"] = "First name is required"
        if not request.last_name:
            errors["last_name"] = "Last name is required"

        return errors if errors else None

    def _is_valid_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def _is_strong_password(self, password: str) -> bool:
        """Check if password meets strength requirements"""
        has_upper = re.search(r"[A-Z]", password)
        has_lower = re.search(r"[a-z]", password)
        has_digit = re.search(r"\d", password)
        has_special = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)

        return all([has_upper, has_lower, has_digit, has_special])

    # def _send_verification_email(self, email: str, user_id: str) -> None:
    #     """Send email verification"""
    #     if self.email_service:
    #         verification_token = secrets.token_urlsafe(32)
    #         # Store token in database or cache
    #         # Send email with verification link
    #         self.email_service.send_verification_email(email, verification_token)
