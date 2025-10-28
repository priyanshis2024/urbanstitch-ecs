"""This module handles request body, response body and field validation"""

from typing import Optional
from fastapi_camelcase import CamelModel
from pydantic import Field, EmailStr
from uuid import UUID
from datetime import datetime


class ContactUsCreate(CamelModel):
    user_id: UUID = Field(
        ..., title="User ID", description="The unique identifier of the user"
    )
    message: str = Field(
        ..., title="Topic", description="Topic or message of why you have connected"
    )


class ContactUsResponse(CamelModel):
    id: UUID = Field(
        ...,
        title="ID",
        description="The unique identifier of the person who has connted by using contact us",
    )
    user_id: UUID = Field(
        ..., title="User ID", description="The unique identifier of the user"
    )
    message: str = Field(
        ..., title="Topic", description="Topic or message of why you have connected"
    )
    created_at: Optional[datetime] = Field(
        None,
        title="Created At",
        description="The timestamp when the contact us details were created",
    )
    updated_at: Optional[datetime] = Field(
        None,
        title="Updated At",
        description="The timestamp when the contact us details were last updated",
    )

    class Config:
        orm_mode = True


class ContactUsUpdate(CamelModel):
    message: str = Field(
        ..., title="Topic", description="Topic or message of why you have connected"
    )
