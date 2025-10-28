"""This module handles request body, response body and field validation"""

from fastapi_camelcase import CamelModel
from pydantic import Field
from uuid import UUID
from datetime import datetime
from typing import List, Optional


class SizeCreate(CamelModel):
    id: UUID = Field(..., title="ID", description="The unique identifier of the size")
    size: str = Field(..., title="Size", description="The Size of the product")
    data: dict = Field(
        ..., title="Data", description="The size-related details for the product"
    )


class SizeResponse(CamelModel):
    id: UUID = Field(..., title="ID", description="The unique identifier of the size")
    size: str = Field(..., title="Size", description="The Size of the product")
    data: dict = Field(
        ..., title="Data", description="The size related details for the product"
    )
    created_at: Optional[datetime] = Field(
        None,
        title="Created At",
        description="The timestamp when the size details were created",
    )
    updated_at: Optional[datetime] = Field(
        None,
        title="Updated At",
        description="The timestamp when the size details were last updated",
    )
    created_by: Optional[str] = Field(
        ...,
        title="Created By",
        description="Name of person who has created this size details",
    )
    updated_by: Optional[str] = Field(
        ...,
        title="Updated By",
        description="Name of person who has updated this size details",
    )


class SizeListResponse(CamelModel):
    total_size_count: int
    sizes: List[SizeResponse] = []


class SizeUpdate(CamelModel):
    size: Optional[str] = Field(
        None, title="Size", description="The Size of the product"
    )
    data: Optional[dict] = Field(
        None, title="Data", description="The size related details for the product"
    )


class SizeBulkResponse(CamelModel):
    created_size_count: int
    existing_size_count: int
    data: List[SizeResponse]
    created_size_ids: List[UUID]
    existing_size_ids: List[UUID]
