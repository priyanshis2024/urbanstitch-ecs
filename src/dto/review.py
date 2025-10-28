"""This module handles request body, response body and field validation"""

from typing import Optional
from fastapi_camelcase import CamelModel
from pydantic import Field
from uuid import UUID
from datetime import datetime
from typing import List


class ReviewCreate(CamelModel):
    product_id: UUID = Field(
        ..., title="Product ID", description="The unique identifier of the product"
    )
    rating: Optional[int] = Field(
        None,
        title="Rating",
        description="The rating of the user on product",
        ge=1,
        le=5,
    )
    review: Optional[str] = Field(
        None, title="First Name", description="The first name of the user"
    )
    image: Optional[str] = Field(
        None, title="Image", description="Review image for the product"
    )


class ReviewResponse(CamelModel):
    id: UUID = Field(..., title="ID", description="The unique identifier of the review")
    product_id: UUID = Field(
        ..., title="Product ID", description="The unique identifier of the product"
    )
    user_id: str = Field(
        ..., title="User ID", description="The unique identifier of the User"
    )
    rating: Optional[int] = Field(
        ..., title="Rating", description="The rating of the user on product"
    )
    review: Optional[str] = Field(
        ..., title="First Name", description="The first name of the user"
    )
    image: Optional[str] = Field(
        ..., title="Image", description="Review image for the product"
    )
    is_rated: int = Field(
        ..., title="Rating", description="The rating of the user given on the product"
    )
    created_at: Optional[datetime] = Field(
        None,
        title="Created At",
        description="The timestamp when the review details were created",
    )
    updated_at: Optional[datetime] = Field(
        None,
        title="Updated At",
        description="The timestamp when the review details were last updated",
    )

    class Config:
        orm_mode = True


class ReviewListResponse(CamelModel):
    total_review_count: int
    reviews: List[ReviewResponse]


class ReviewUpdate(CamelModel):
    product_id: UUID = Field(
        None, title="Product ID", description="The unique identifier of the product"
    )
    rating: Optional[int] = Field(
        None,
        title="Rating",
        description="The rating of the user on product",
        ge=1,
        le=5,
    )
    review: Optional[str] = Field(
        None, title="First Name", description="The first name of the user"
    )
    image: Optional[str] = Field(
        None, title="Image", description="Review image for the product"
    )
