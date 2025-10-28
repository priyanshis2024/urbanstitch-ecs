"""This module handles request body, response body and field validation"""

from typing import List, Optional, Union
from fastapi_camelcase import CamelModel
from pydantic import Field, field_validator
from uuid import UUID
from datetime import datetime


class WishlistCreate(CamelModel):
    subproduct_id: UUID = Field(
        ..., title="Subproduct ID", description="The unique identifier of subproduct"
    )


class WishlistResponse(CamelModel):
    id: UUID = Field(
        ..., title="ID", description="The unique identifier of the wishlist"
    )
    user_id: str = Field(
        ..., title="User ID", description="The unique identifier of the user"
    )
    subproduct_id: UUID = Field(
        ..., title="Subproduct ID", description="The unique identifier of subproduct"
    )
    created_at: Optional[datetime] = Field(
        None,
        title="Created At",
        description="The timestamp when the wishlist product details were created",
    )
    updated_at: Optional[datetime] = Field(
        None,
        title="Updated At",
        description="The timestamp when the wishlist product details were last updated",
    )

    class Config:
        orm_mode = True


class WishlistDetailResponse(CamelModel):
    id: UUID = Field(
        ..., title="ID", description="The unique identifier of the wishlist"
    )
    subproduct_id: UUID = Field(
        ..., title="Subproduct ID", description="The unique identifier of subproduct"
    )
    name: str = Field(..., title="Name", description="The product name")
    description: str = Field(
        ..., title="Description", description="Description of product"
    )
    price: int = Field(..., title="Price", description="The price of the subproduct")
    rating: Optional[float] = Field(
        None,
        title="Rating",
        description="The rating of the overall product given by all users",
    )
    images: List[str] = Field(..., title="Image", description="Product image")

    @field_validator("images", mode="before")
    @classmethod
    def split_images(cls, v: Union[str, List[str]]):
        if isinstance(v, str):
            return v.split(",")
        return v


class WishlistListDetailResponse(CamelModel):
    total_wishlist_product_count: int
    wishlist_products: List[WishlistDetailResponse]
