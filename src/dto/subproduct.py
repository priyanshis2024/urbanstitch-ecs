"""This module handles request body, response body and field validation"""

from fastapi_camelcase import CamelModel
from pydantic import Field, field_validator
from uuid import UUID
from datetime import datetime
from typing import List, Union, Optional
from src.dto.size import SizeCreate


class SubproductCreate(CamelModel):
    id: UUID = Field(
        ..., title="ID", description="The unique identifier of the subproduct"
    )
    product_id: UUID = Field(
        ..., title="Product ID", description="The unique identifier of product"
    )
    size_id: UUID = Field(
        ..., title="Size ID", description="The unique identifier of the size"
    )
    price: int = Field(..., title="Price", description="The price of the subproduct")
    color: Optional[str] = Field(None, title="Color", description="Product color")
    quantity: int = Field(
        ...,
        title="Quantity",
        description="The total quantity of the product according to their size and color",
    )
    images: List[str] = Field(..., title="Image", description="Product image")
    status: Optional[int] = Field(
        None, title="Status", description="The status of the product"
    )
    sizes: Optional[List[SizeCreate]] = []

    @field_validator("images", mode="before")
    @classmethod
    def split_images(cls, v: Union[str, List[str]]):
        if isinstance(v, str):
            return v.split(",")
        return v


class SubproductResponse(CamelModel):
    id: UUID = Field(
        ..., title="ID", description="The unique identifier of the subproduct"
    )
    product_id: UUID = Field(
        ..., title="Product ID", description="The unique identifier of product"
    )
    size_id: UUID = Field(
        ..., title="Size ID", description="The unique identifier of the size"
    )
    price: int = Field(..., title="Price", description="The price of the subproduct")
    color: Optional[str] = Field(None, title="Color", description="Product color")
    quantity: int = Field(
        ...,
        title="Quantity",
        description="The total quantity of the product according to their size and color",
    )
    images: List[str] = Field(..., title="Image", description="Product image")
    status: Optional[int] = Field(
        None, title="Status", description="The status of the product"
    )
    created_by: Optional[str] = Field(
        ...,
        title="Created By",
        description="Name of person who has created this subproduct details",
    )
    updated_by: Optional[str] = Field(
        ...,
        title="Updated By",
        description="Name of person who has updated this subproduct details",
    )
    created_at: Optional[datetime] = Field(
        None,
        title="Created At",
        description="The timestamp when the subproduct details were created",
    )
    updated_at: Optional[datetime] = Field(
        None,
        title="Updated At",
        description="The timestamp when the subproduct details were last updated",
    )

    @field_validator("images", mode="before")
    @classmethod
    def split_images(cls, v: Union[str, List[str]]):
        if isinstance(v, str):
            return v.split(",")
        return v


class SubproductUpdate(CamelModel):
    product_id: Optional[UUID] = Field(
        None, title="Product ID", description="The unique identifier of the product"
    )
    size_id: Optional[UUID] = Field(
        None, title="Size ID", description="The unique identifier of the size"
    )
    price: Optional[int] = Field(
        None, title="Price", description="The price of the subproduct"
    )
    color: Optional[str] = Field(None, title="Color", description="Product color")
    quantity: Optional[int] = Field(
        None,
        title="Quantity",
        description="The total quantity of the product according to their size and color",
    )
    images: Optional[List[str]] = Field(
        default_factory=list, title="Image", description="Product image"
    )
    status: Optional[int] = Field(
        None, title="Status", description="The status of the product"
    )

    @field_validator("images", mode="before")
    @classmethod
    def split_images(cls, v: Union[str, List[str]]):
        if isinstance(v, str):
            return v.split(",")
        return v


class SubproductListingResponse(CamelModel):
    id: UUID = Field(
        ..., title="ID", description="The unique identifier of the subproduct"
    )
    product_id: UUID = Field(
        ..., title="Product ID", description="The unique identifier of product"
    )
    category_xref_id: UUID = Field(
        ...,
        title="Category xref ID mapping ID",
        description="The unique identifier of Category and Subcategory mapping ID",
    )
    category_id: UUID = Field(
        ..., title="ID", description="The unique identifier of the category"
    )
    subcategory_id: UUID = Field(
        ..., title="ID", description="The unique identifier of the subcategory"
    )
    brand_id: UUID = Field(
        ..., title="Brand ID", description="The unique identifier of the brand"
    )
    name: str = Field(..., title="Name", description="The product name")
    description: str = Field(
        ..., title="Description", description="Description of product"
    )
    rating: Optional[float] = Field(
        None,
        title="Rating",
        description="The rating of the overall product given by all users",
    )
    price: int = Field(..., title="Price", description="The price of the subproduct")
    color: Optional[str] = Field(None, title="Color", description="Product color")
    quantity: int = Field(
        ...,
        title="Quantity",
        description="The total quantity of the product according to their size and color",
    )
    images: List[str] = Field(..., title="Image", description="Product image")

    @field_validator("images", mode="before")
    @classmethod
    def split_images(cls, v: Union[str, List[str]]):
        if isinstance(v, str):
            return v.split(",")
        return v

    @field_validator("rating", mode="before")
    def result_check(cls, v):
        ...
        return round(v, 1)


class SubproductDetailResponse(CamelModel):
    id: UUID = Field(
        ..., title="ID", description="The unique identifier of the subproduct"
    )
    product_id: UUID = Field(
        ..., title="Product ID", description="The unique identifier of product"
    )
    category_xref_id: UUID = Field(
        ...,
        title="Category xref ID mapping ID",
        description="The unique identifier of Category and Subcategory mapping ID",
    )
    category_id: UUID = Field(
        ..., title="ID", description="The unique identifier of the category"
    )
    subcategory_id: UUID = Field(
        ..., title="ID", description="The unique identifier of the subcategory"
    )
    brand_id: UUID = Field(
        ..., title="Brand ID", description="The unique identifier of the brand"
    )
    size_id: UUID = Field(
        ..., title="Size ID", description="The unique identifier of the size"
    )
    size: str = Field(..., title="Size", description="The size of the subproduct")
    name: str = Field(..., title="Name", description="The product name")
    description: str = Field(
        ..., title="Description", description="Description of product"
    )
    data: Optional[dict] = Field(
        None,
        title="Long description",
        description="The long description of the product",
    )
    fabric: Optional[str] = Field(
        None, title="Fabric", description="The product fabric name"
    )
    rating: Optional[float] = Field(
        None,
        title="Rating",
        description="The rating of the overall product given by all users",
    )
    price: int = Field(..., title="Price", description="The price of the subproduct")
    color: Optional[str] = Field(None, title="Color", description="Product color")
    quantity: int = Field(
        ...,
        title="Quantity",
        description="The total quantity of the product according to their size and color",
    )
    images: List[str] = Field(..., title="Image", description="Product image")

    @field_validator("images", mode="before")
    @classmethod
    def split_images(cls, v: Union[str, List[str]]):
        if isinstance(v, str):
            return v.split(",")
        return v

    @field_validator("rating", mode="before")
    def result_check(cls, v):
        ...
        return round(v, 1)


class SubproductDetailListResponse(CamelModel):
    total_subproduct_count: int
    subproducts: List[SubproductListingResponse]


class SubproductUpdateStatus(CamelModel):
    status: int = Field(
        ...,
        title="Subproduct status",
        description="Subproduct status to check if they are disable, enable or blocked.",
    )


class SubproductSizeResponse(CamelModel):
    id: UUID = Field(
        ..., title="ID", description="The unique identifier of the subproduct"
    )
    product_id: UUID = Field(
        ..., title="Product ID", description="The unique identifier of product"
    )
    size_id: UUID = Field(
        ..., title="Size ID", description="The unique identifier of the size"
    )
    size: str = Field(..., title="Size", description="The size of the subproduct")
    data: Optional[dict] = Field(
        None,
        title="Size details",
        description="The size details of the product",
    )
    price: int = Field(..., title="Price", description="The price of the subproduct")
    color: Optional[str] = Field(None, title="Color", description="Product color")
    quantity: int = Field(
        ...,
        title="Quantity",
        description="The total quantity of the product according to their size and color",
    )
    images: List[str] = Field(..., title="Image", description="Product image")
    status: Optional[int] = Field(
        None, title="Status", description="The status of the product"
    )
    created_by: Optional[str] = Field(
        ...,
        title="Created By",
        description="Name of person who has created this subproduct details",
    )
    updated_by: Optional[str] = Field(
        ...,
        title="Updated By",
        description="Name of person who has updated this subproduct details",
    )
    created_at: Optional[datetime] = Field(
        None,
        title="Created At",
        description="The timestamp when the subproduct details were created",
    )
    updated_at: Optional[datetime] = Field(
        None,
        title="Updated At",
        description="The timestamp when the subproduct details were last updated",
    )

    @field_validator("images", mode="before")
    @classmethod
    def split_images(cls, v: Union[str, List[str]]):
        if isinstance(v, str):
            return v.split(",")
        return v


class SubproductBulkResponse(CamelModel):
    created_subproduct_count: int
    existing_subproduct_count: int
    data: List[SubproductResponse]
    created_subproduct_ids: List[UUID]
    existing_subproduct_ids: List[UUID]
