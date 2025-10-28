"""This module handles request body, response body and field validation"""

from typing import Optional
from fastapi_camelcase import CamelModel
from pydantic import Field
from datetime import datetime


class UserRoleCreate(CamelModel):
    id: int = Field(
        ..., title="ID", description="The unique identifier of the user role"
    )
    role: str = Field(..., title="User role", description="User role for the user")


class UserRoleResponse(CamelModel):
    id: int = Field(
        ..., title="ID", description="The unique identifier of the user role"
    )
    role: str = Field(..., title="User role", description="User role for the user")
    created_at: Optional[datetime] = Field(
        None,
        title="Created At",
        description="The timestamp when the user role details were created",
    )
    updated_at: Optional[datetime] = Field(
        None,
        title="Updated At",
        description="The timestamp when the user role details were last updated",
    )

    class Config:
        orm_mode = True


class UserRoleUpdate(CamelModel):
    role: str = Field(..., title="User role", description="User role for the user")
