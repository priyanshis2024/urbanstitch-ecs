"""This module handles request body, response body and field validation"""

from typing import List, Optional, Union
from fastapi_camelcase import CamelModel
from pydantic import Field, field_validator
from uuid import UUID
from datetime import datetime


class CartCreate(CamelModel):
    subproduct_id: UUID = Field(
        ..., title="Subproduct ID", description="The unique identifier of subproduct"
    )
    order_quantity: Optional[int] = Field(
        None, title="Quantity", description="The total order quantity of the product"
    )


class CartResponse(CamelModel):
    id: UUID = Field(
        ..., title="ID", description="The unique identifier of the cart product"
    )
    subproduct_id: UUID = Field(
        ..., title="Subproduct ID", description="The unique identifier of subproduct"
    )
    user_id: str = Field(
        ..., title="User ID", description="The unique identifier of user"
    )
    order_quantity: int = Field(
        ..., title="Quantity", description="The total order quantity of the product"
    )
    created_at: Optional[datetime] = Field(
        None,
        title="Created At",
        description="The timestamp when the cart product details were created",
    )
    updated_at: Optional[datetime] = Field(
        None,
        title="Updated At",
        description="The timestamp when the cart product details were last updated",
    )

    class Config:
        orm_mode = True


class CartListResponse(CamelModel):
    total_cart_product_count: int
    cart_products: List[CartResponse]


class CartUpdate(CamelModel):
    subproduct_id: Optional[UUID] = Field(
        None, title="Subproduct ID", description="The unique identifier of subproduct"
    )
    order_quantity: Optional[int] = Field(
        None, title="Quantity", description="The total order quantity of the product"
    )


class CartDetailResponse(CamelModel):
    id: UUID = Field(
        ..., title="ID", description="The unique identifier of the cart product"
    )
    subproduct_id: Optional[UUID] = Field(
        None, title="Subproduct ID", description="The unique identifier of subproduct"
    )
    name: str = Field(..., title="Name", description="The product name")
    description: str = Field(
        ..., title="Description", description="Description of product"
    )
    color: str = Field(..., title="Color", description="The color of the product")
    size: str = Field(..., title="Size", description="The Size of the product")
    order_quantity: Optional[int] = Field(
        None, title="Quantity", description="The total order quantity of the product"
    )
    price: int = Field(..., title="Price", description="The price of the subproduct")
    images: List[str] = Field(..., title="Image", description="Product image")

    @field_validator("images", mode="before")
    @classmethod
    def split_images(cls, v: Union[str, List[str]]):
        if isinstance(v, str):
            return v.split(",")
        return v


class CartListDetailResponse(CamelModel):
    total_cart_product_count: int
    cart_products: List[CartDetailResponse]


class ProductDTO(CamelModel):
    id: str
    name: str
    color: str
    size: str
    quantity: int
    price: float


class CheckoutSessionRequest(CamelModel):
    products: List[ProductDTO]
    payment_id: str
    order_id: str


class CheckoutSessionResponse(CamelModel):
    id: str
    object: Optional[str]
    url: Optional[str]
    payment_status: Optional[str]
    payment_method_types: Optional[List[str]]
    shipping_cost: Optional[int]
    amount_total: Optional[float]
    amount_subtotal: Optional[float]
    customer: Optional[str]
    customer_email: Optional[str]
    customer_details: Optional[str]
    payment_link: Optional[str]
    status: Optional[str]
    session: Optional[str]
    line_items: list
