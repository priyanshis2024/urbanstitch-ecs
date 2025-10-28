"""This module handles request body, response body and field validation"""

from typing import Optional, List
from fastapi_camelcase import CamelModel
from pydantic import Field
from uuid import UUID
from datetime import datetime


class SubcategoryResponse(CamelModel):
    id: UUID = Field(
        ..., title="ID", description="The unique identifier of the subcategory"
    )
    name: str = Field(..., title="Name", description="The subcategory name")
    status: int = Field(..., title="Status", description="The status of the categories")
    created_at: Optional[datetime] = Field(
        None,
        title="Created At",
        description="The timestamp when the subcategory details were created",
    )
    updated_at: Optional[datetime] = Field(
        None,
        title="Updated At",
        description="The timestamp when the subcategory details were last updated",
    )
    created_by: Optional[str] = Field(
        ...,
        title="Created By",
        description="Name of person who has created this subcategory details",
    )
    updated_by: Optional[str] = Field(
        ...,
        title="Updated By",
        description="Name of person who has updated this subcategory details",
    )

    class Config:
        orm_mode = True
        populate_by_name = True


class Subcategorydetail(CamelModel):
    id: UUID = Field(
        ..., title="ID", description="The unique identifier of the subcategory"
    )
    name: str = Field(..., title="Name", description="The subcategory name")
    status: int = Field(
        ..., title="Status", description="The status of the subcategories"
    )


class SubcategoryCreate(CamelModel):
    id: UUID = Field(
        ..., title="ID", description="The unique identifier of the subcategory"
    )
    name: str = Field(..., title="Name", description="The subcategory name")
    status: Optional[int] = Field(
        None, title="Status", description="The status of the subcategories"
    )
    subcategories_type: str = Field(
        ..., title="Subcategories Type", description="The type of the subcategory"
    )


class SubcategoryUpdate(CamelModel):
    id: UUID = Field(
        ..., title="ID", description="The unique identifier of subcategory ID"
    )
    name: Optional[str] = Field(
        ..., title="Name", description="The subcategory subcategory"
    )
    status: Optional[int] = Field(
        None, title="Status", description="The status of the subcategories"
    )


class SubcategoryDeleteRequest(CamelModel):
    id: UUID
    name: Optional[str] = None  # Name is optional, mainly for response clarity


class SubcategoryUpdateStatus(CamelModel):
    status: int = Field(
        ...,
        title="Subcategory status",
        description="Subcategory status to check if they are disable, enable or blocked.",
    )


class Subcategorydetails(CamelModel):
    id: UUID = Field(
        ..., title="ID", description="The unique identifier of the subcategory"
    )
    name: str = Field(..., title="Name", description="The subcategory name")
    status: int = Field(..., title="Status", description="The status of the categories")
    created_at: Optional[datetime] = Field(
        None,
        title="Created At",
        description="The timestamp when the subcategory details were created",
    )
    updated_at: Optional[datetime] = Field(
        None,
        title="Updated At",
        description="The timestamp when the subcategory details were last updated",
    )
    created_by: Optional[str] = Field(
        ...,
        title="Created By",
        description="Name of person who has created this subcategory details",
    )
    updated_by: Optional[str] = Field(
        ...,
        title="Updated By",
        description="Name of person who has updated this subcategory details",
    )

    class Config:
        orm_mode = True


class SubcategoryDetailListResponse(CamelModel):
    total_subcategories_count: int
    subcategories: List[Subcategorydetails]

    class Config:
        orm_mode = True


class XrefSubcategoryResponse(CamelModel):
    subcategories_type: str = Field(
        Field(
            ...,
            title="Subcategories type",
            description="The subcategory type which identify the type of the subcategory",
        )
    )
    total_subcategories_count: int
    subcategories: List[Subcategorydetail]
