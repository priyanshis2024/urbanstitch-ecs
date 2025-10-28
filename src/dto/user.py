"""This module handles request body, response body and field validation"""

from typing import Optional
from fastapi_camelcase import CamelModel
from pydantic import Field, EmailStr, field_validator
from uuid import UUID
from typing import List
from datetime import datetime, date
from src.utils.utils import (
    validate_if_alphabet,
    validate_date,
    validate_email,
    validate_password,
    validate_phone_number,
)


class UserCreate(CamelModel):
    id: Optional[UUID] = Field(
        None, title="ID", description="The unique identifier of the user"
    )
    user_role_id: int = Field(
        ..., title="User role ID", description="The unique identifier of the user role"
    )
    contact: str = Field(
        ..., title="Contact Number", description="The phone number of the user"
    )
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
    username: Optional[str] = Field(
        None, title="User Name", description="The first name of the user"
    )
    image: Optional[str] = Field(None, title="Image", description="User profile image")
    first_name: str = Field(
        ..., title="First Name", description="The first name of the user"
    )
    last_name: str = Field(
        ..., title="Last Name", description="The last name of the user"
    )
    gender: Optional[int] = Field(
        None, title="Gender", description="The gender of the user"
    )
    dob: Optional[date] = Field(
        None, title="Date of birth", description="The Date of birth of the user"
    )
    status: int = Field(
        ...,
        title="User status",
        description="User status to check if they are disable, enable or blocked.",
    )

    @field_validator("first_name")
    def validate_first_name(cls, value: str) -> str:
        """
        Validate the first name to ensure it contains only alphabets.
        """
        return validate_if_alphabet(value)

    @field_validator("last_name")
    def validate_last_name(cls, value: str) -> str:
        """
        Validate the last name to ensure it contains only alphabets.
        """
        return validate_if_alphabet(value)

    @field_validator("contact")
    def validate_contact(cls, value: str) -> str:
        """
        Validate the contact number to ensure it is a valid phone number.
        """
        return validate_phone_number(value)

    @field_validator("email")
    def validate_email(cls, value: str) -> str:
        """
        Validate the email address to ensure it is valid.
        """
        return validate_email(value)

    @field_validator("dob")
    def validate_dob(cls, value: date) -> date:
        """
        Validate the date of birth to ensure it is not in the future.
        """
        return validate_date(value)


class UserResponse(CamelModel):
    id: UUID = Field(..., title="ID", description="The unique identifier of the user")
    user_role_id: int = Field(
        ..., title="User role ID", description="The unique identifier of the user role"
    )
    contact: str = Field(
        ..., title="Contact Number", description="The phone number of the user"
    )
    email: EmailStr = Field(
        ..., title="Email", description="The email address of the user"
    )
    password: str = Field(
        ..., title="Hashed password", description="Hashed password of user"
    )
    username: Optional[str] = Field(
        None, title="User Name", description="The first name of the user"
    )
    image: Optional[str] = Field(None, title="Image", description="User profile image")
    first_name: Optional[str] = Field(
        None, title="First Name", description="The first name of the user"
    )
    last_name: Optional[str] = Field(
        None, title="Last Name", description="The last name of the user"
    )
    gender: Optional[int] = Field(
        None, title="Gender", description="The gender of the user"
    )
    dob: Optional[date] = Field(
        None, title="Date of birth", description="The Date of birth of the user"
    )
    status: int = Field(..., title="Status", description="The status of the user")
    created_at: Optional[datetime] = Field(
        None,
        title="Created At",
        description="The timestamp when the user details were created",
    )
    updated_at: Optional[datetime] = Field(
        None,
        title="Updated At",
        description="The timestamp when the user details were last updated",
    )

    class Config:
        orm_mode = True


class UserListResponse(CamelModel):
    total_user_count: int
    Users: List[UserResponse]


class UserUpdate(CamelModel):
    user_role_id: Optional[int] = Field(
        None, title="User role ID", description="The unique identifier of the user role"
    )
    contact: Optional[str] = Field(
        None, title="Contact Number", description="The phone number of the user"
    )
    email: Optional[EmailStr] = Field(
        None, title="Email", description="The email address of the user"
    )
    password: Optional[str] = Field(
        None, title="Hashed password", description="Hashed password of user"
    )
    username: Optional[str] = Field(
        None, title="User Name", description="The first name of the user"
    )
    image: Optional[str] = Field(None, title="Image", description="User profile image")
    first_name: Optional[str] = Field(
        None, title="First Name", description="The first name of the user"
    )
    last_name: Optional[str] = Field(
        None, title="Last Name", description="The last name of the user"
    )
    gender: Optional[int] = Field(
        None, title="Gender", description="The gender of the user"
    )
    dob: Optional[date] = Field(
        None, title="Date of birth", description="The Date of birth of the user"
    )
    status: Optional[int] = Field(
        None,
        title="User status",
        description="User status to check if they are disable, enable or blocked.",
    )


class UserUpdateStatus(CamelModel):
    status: int = Field(
        ...,
        title="User status",
        description="User status to check if they are disable, enable or blocked.",
    )


class UserCreationResponse(CamelModel):
    is_user_created: bool = Field(
        ...,
        title="User creation status",
        description="This field checks if user is created or not.",
    )
    id: Optional[UUID] = Field(
        None, title="ID", description="The unique identifier of the user"
    )
    user_role_id: int = Field(
        ..., title="User role ID", description="The unique identifier of the user role"
    )
    contact: str = Field(
        ..., title="Contact Number", description="The phone number of the user"
    )
    email: EmailStr = Field(
        ..., title="Email", description="The email address of the user"
    )
    password: str = Field(
        ..., title="Hashed password", description="Hashed password of user"
    )
    username: Optional[str] = Field(
        None, title="User Name", description="The first name of the user"
    )
    image: Optional[str] = Field(None, title="Image", description="User profile image")
    first_name: str = Field(
        ..., title="First Name", description="The first name of the user"
    )
    last_name: str = Field(
        ..., title="Last Name", description="The last name of the user"
    )
    gender: Optional[int] = Field(
        None, title="Gender", description="The gender of the user"
    )
    dob: Optional[date] = Field(
        None, title="Date of birth", description="The Date of birth of the user"
    )
    status: int = Field(..., title="Status", description="The status of the user")
    created_at: Optional[datetime] = Field(
        None,
        title="Created At",
        description="The timestamp when the user details were created",
    )
    updated_at: Optional[datetime] = Field(
        None,
        title="Updated At",
        description="The timestamp when the user details were last updated",
    )

    class Config:
        orm_mode = True


class OTPResponse(CamelModel):
    otp: str = Field(
        ...,
        title="OTP (One time password)",
        description="One time password for the sign up",
    )
