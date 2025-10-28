"""This module handles request body, response body and field validation"""

from typing import Optional
from fastapi_camelcase import CamelModel
from pydantic import Field, EmailStr, field_validator
from uuid import UUID
from datetime import datetime
from src.utils.utils import (
    validate_if_alphabet,
    validate_email,
    validate_phone_number,
)


class CustomerDetailCreate(CamelModel):
    address_type: int = Field(..., title="Address type", description="Address type")
    address: str = Field(..., title="Address", description="Whole address of user")
    landmark: str = Field(
        ..., title="Landmark", description="The landmark of the user's address"
    )
    city: str = Field(..., title="City", description="The city of user's address")
    state: str = Field(..., title="State", description="The State of user's address")
    country: str = Field(
        ..., title="Country", description="The country name of the user's address"
    )
    pincode: int = Field(
        ..., title="Pincode", description="The pincode of user's address"
    )
    contact: str = Field(
        ..., title="Contact Number", description="The phone number of the user"
    )
    email: EmailStr = Field(
        ..., title="Email", description="The email address of the user"
    )
    first_name: str = Field(
        ..., title="First Name", description="The first name of the user"
    )
    last_name: str = Field(
        ..., title="Last Name", description="The last name of the user"
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


class CustomerDetailResponse(CamelModel):
    id: UUID = Field(
        ..., title="ID", description="The unique identifier of the address"
    )
    user_id: UUID = Field(
        ..., title="User ID", description="The unique identifier of the user"
    )
    address_type: int = Field(..., title="Address type", description="Address type")
    address: str = Field(..., title="Address", description="Whole address of user")
    landmark: str = Field(
        ..., title="Landmark", description="The landmark of the user's address"
    )
    city: str = Field(..., title="City", description="The city of user's address")
    state: str = Field(..., title="State", description="The State of user's address")
    country: str = Field(
        ..., title="Country", description="The country name of the user's address"
    )
    pincode: int = Field(
        ..., title="Pincode", description="The pincode of user's address"
    )
    contact: str = Field(
        ..., title="Contact Number", description="The phone number of the user"
    )
    email: EmailStr = Field(
        ..., title="Email", description="The email address of the user"
    )
    first_name: str = Field(
        ..., title="First Name", description="The first name of the user"
    )
    last_name: str = Field(
        ..., title="Last Name", description="The last name of the user"
    )
    created_at: Optional[datetime] = Field(
        None,
        title="Created At",
        description="The timestamp when the Address details were created",
    )
    updated_at: Optional[datetime] = Field(
        None,
        title="Updated At",
        description="The timestamp when the Address details were last updated",
    )

    class Config:
        orm_mode = True


class CustomerDetailUpdate(CamelModel):
    address_type: Optional[int] = Field(
        None, title="Address type", description="Address type"
    )
    address: Optional[str] = Field(
        None, title="Address", description="Whole address of user"
    )
    landmark: Optional[str] = Field(
        None, title="Landmark", description="The landmark of the user's address"
    )
    city: Optional[str] = Field(
        None, title="City", description="The city of user's address"
    )
    state: Optional[str] = Field(
        None, title="State", description="The State of user's address"
    )
    country: Optional[str] = Field(
        None, title="Country", description="The country name of the user's address"
    )
    pincode: Optional[int] = Field(
        None, title="Pincode", description="The pincode of user's address"
    )
    contact: Optional[str] = Field(
        None, title="Contact Number", description="The phone number of the user"
    )
    email: Optional[EmailStr] = Field(
        None, title="Email", description="The email address of the user"
    )
    first_name: Optional[str] = Field(
        None, title="First Name", description="The first name of the user"
    )
    last_name: Optional[str] = Field(
        None, title="Last Name", description="The last name of the user"
    )


class CustomerDetailListResponse(CamelModel):
    total_customer_details_count: int
    customer_details: list[CustomerDetailResponse]
