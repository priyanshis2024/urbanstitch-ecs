"""This module handles request body, response body and field validation"""

from typing import Optional
from fastapi_camelcase import CamelModel
from pydantic import Field
from uuid import UUID
from datetime import datetime
from typing import List
from src.dto.subcategory import (
    SubcategoryCreate,
    SubcategoryDeleteRequest,
    Subcategorydetail,
    SubcategoryUpdate,
)


class CategoryResponse(CamelModel):
    id: UUID = Field(
        ..., title="ID", description="The unique identifier of the category"
    )
    name: str = Field(..., title="Name", description="The category name")
    status: int = Field(..., title="Status", description="The status of the categories")
    created_at: Optional[datetime] = Field(
        None,
        title="Created At",
        description="The timestamp when the category details were created",
    )
    updated_at: Optional[datetime] = Field(
        None,
        title="Updated At",
        description="The timestamp when the category details were last updated",
    )
    created_by: Optional[str] = Field(
        ...,
        title="Created By",
        description="Name of person who has created this category details",
    )
    updated_by: Optional[str] = Field(
        ...,
        title="Updated By",
        description="Name of person who has updated this category details",
    )
    total_subcategories_count: int
    subcategories: Optional[List[Subcategorydetail]] = []

    class Config:
        orm_mode = True
        populate_by_name = True


class Categorydetails(CamelModel):
    id: UUID = Field(
        ..., title="ID", description="The unique identifier of the category"
    )
    name: str = Field(..., title="Name", description="The category name")
    status: int = Field(..., title="Status", description="The status of the categories")
    created_at: Optional[datetime] = Field(
        None,
        title="Created At",
        description="The timestamp when the category details were created",
    )
    updated_at: Optional[datetime] = Field(
        None,
        title="Updated At",
        description="The timestamp when the category details were last updated",
    )
    created_by: Optional[str] = Field(
        ...,
        title="Created By",
        description="Name of person who has created this category details",
    )
    updated_by: Optional[str] = Field(
        ...,
        title="Updated By",
        description="Name of person who has updated this category details",
    )

    class Config:
        orm_mode = True


class CategoryDetailListResponse(CamelModel):
    total_categories_count: int
    categories: List[Categorydetails]

    class Config:
        orm_mode = True


class CategoryListResponse(CamelModel):
    total_categories_count: int
    categories: List[CategoryResponse]

    class Config:
        orm_mode = True
        populate_by_name = True


class CategoryCreate(CamelModel):
    id: UUID = Field(
        ..., title="ID", description="The unique identifier of the category"
    )
    name: str = Field(..., title="Name", description="The category name")
    status: Optional[int] = Field(
        None, title="Status", description="The status of the categories"
    )
    subcategories: Optional[List[SubcategoryCreate]] = []


class Categorycreation(CamelModel):
    id: UUID = Field(
        ..., title="ID", description="The unique identifier of the category"
    )
    name: str = Field(..., title="Name", description="category name")
    status: Optional[int] = Field(
        None, title="Status", description="The status of the categories"
    )

    class Config:
        from_attributes = True


class Subcategorycreation(CamelModel):
    id: UUID = Field(
        ..., title="ID", description="The unique identifier of the subcategory"
    )
    name: str = Field(..., title="Name", description="The subcategory name")
    status: Optional[int] = Field(
        None, title="Status", description="The status of the subcategories"
    )
    categories: Optional[List[Categorycreation]] = []


class CategoryUpdate(CamelModel):
    name: Optional[str] = Field(..., title="Name", description="The category name")
    status: Optional[int] = Field(
        None, title="Status", description="The status of the categories"
    )
    subcategories: Optional[List[SubcategoryUpdate]] = []


class DeleteCategory(CamelModel):
    name: Optional[str] = Field(..., title="Name", description="The category name")
    subcategories: Optional[List[SubcategoryUpdate]] = []


class DeleteCategoryRequest(CamelModel):
    name: str  # Category name for reference
    subcategories: Optional[List[SubcategoryDeleteRequest]] = None


class DeleteCategoryResponse(CamelModel):
    status: str  # Deletion message
    category_id: UUID
    category_name: str
    deleted_subcategories: Optional[List[SubcategoryDeleteRequest]] = (
        None  # List of deleted subcategories
    )
    remaining_subcategories: Optional[List[SubcategoryDeleteRequest]] = None


class CategoryUpdateStatus(CamelModel):
    status: int = Field(
        ...,
        title="Category status",
        description="Category status to check if they are disable, enable or blocked.",
    )


class CategoryBulkResponse(CamelModel):
    created_categories_count: int
    existing_categories_count: int
    created_subcategories_count: int
    existing_subcategories_count: int
    data: List[CategoryResponse]
    created_categories_ids: List[UUID]
    existing_categories_ids: List[UUID]
    created_subcategories_ids: List[UUID]
    existing_subcategories_ids: List[UUID]
