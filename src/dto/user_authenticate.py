"""This module handles request body, response body and field validation"""

from fastapi_camelcase import CamelModel
from pydantic import Field, EmailStr, field_validator
from uuid import UUID
from datetime import datetime
from src.utils.utils import validate_email
from typing import Optional


class OTPGenerationRequest(CamelModel):
    email: EmailStr = Field(
        ..., title="Email", description="The email address of the user"
    )


class UserLogin(CamelModel):
    email: EmailStr = Field(
        ..., title="Email", description="The email address of the user"
    )
    password: str = Field(
        ..., title="Hashed password", description="Hashed password of user"
    )
    encrypted_aes_key: Optional[str] = Field(
        ..., title="Encrypted AES key", description="Encrypted AES of the user"
    )
    encrypted_aes_iv: Optional[str] = Field(
        ..., title="Encrypted AES IV", description="Encrypted AES IV of the user"
    )

    @field_validator("email")
    def validate_email(cls, value: str) -> str:
        """
        Validate the email address to ensure it is valid.
        """
        return validate_email(value)


class OTPGenerateResponse(CamelModel):
    message: str


class UserAuthenticationCreate(CamelModel):
    """DTO for creating a UserAuthentication record."""

    user_id: UUID
    access_token: str
    refresh_token: str
    expired_at: datetime
