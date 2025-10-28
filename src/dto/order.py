"""This module handles request body, response body and field validation"""

from typing import Optional
from fastapi_camelcase import CamelModel
from pydantic import Field
from uuid import UUID
from datetime import datetime
from typing import List
from src.dto.customer_details import CustomerDetailResponse
from src.dto.payment import PaymentResponse


class OrderCreate(CamelModel):
    user_id: UUID = Field(
        ...,
        title="User ID",
        description="The unique identifier of user table",
    )
    customer_id: str = Field(
        ...,
        title="Customer ID",
        description="The unique identifier of customer details table",
    )
    order_status: int = Field(
        ...,
        title="Order Status",
        description="The order status of your order for tracking order details",
    )


class OrderResponse(CamelModel):
    id: UUID = Field(..., title="ID", description="The unique identifier of the order")
    user_id: str = Field(
        ..., title="User ID", description="The unique identifier of the User"
    )
    customer_id: str = Field(
        ...,
        title="Customer ID",
        description="The unique identifier of customer details table",
    )
    order_status: int = Field(
        ...,
        title="Order Status",
        description="The order status of your order for tracking order details",
    )
    created_at: Optional[datetime] = Field(
        None,
        title="Created At",
        description="The timestamp when the order details were created",
    )
    updated_at: Optional[datetime] = Field(
        None,
        title="Updated At",
        description="The timestamp when the order details were last updated",
    )

    class Config:
        orm_mode = True


class OrderHistoryCreate(CamelModel):
    order_id: UUID = Field(
        ..., title="ID", description="The unique identifier of the order"
    )
    subproduct_id: UUID = Field(
        ..., title="Subproduct ID", description="The unique identifier of subproduct"
    )
    price: int = Field(..., title="Price", description="The price of the subproduct")
    order_quantity: int = Field(
        ..., title="Quantity", description="The total order quantity of the product"
    )


class OrderHistoryResponse(CamelModel):
    id: UUID = Field(
        ..., title="ID", description="The unique identifier of the order history"
    )
    order_id: UUID = Field(
        ..., title="ID", description="The unique identifier of the order"
    )
    subproduct_id: UUID = Field(
        ..., title="Subproduct ID", description="The unique identifier of subproduct"
    )
    price: int = Field(..., title="Price", description="The price of the subproduct")
    order_quantity: int = Field(
        ..., title="Quantity", description="The total order quantity of the product"
    )
    created_at: Optional[datetime] = Field(
        None,
        title="Created At",
        description="The timestamp when the order history details were created",
    )
    updated_at: Optional[datetime] = Field(
        None,
        title="Updated At",
        description="The timestamp when the order history details were last updated",
    )


class OrderHistoryListResponse(CamelModel):
    total_product_count: int
    products: List[OrderHistoryResponse]


class UserOrderResponse(CamelModel):
    order: OrderResponse
    order_products: OrderHistoryListResponse


class UserOrderCreationResponse(UserOrderResponse):
    total_order_amount: float = Field(
        ...,
        title="Total Amount",
        description="The total amount of the order",
    )


class OrderSummaryResponse(UserOrderCreationResponse):
    customer_details: CustomerDetailResponse
    payment_details: PaymentResponse


class UserOrderSummaryResponse(CamelModel):
    total_order_count: int
    orders: list[UserOrderResponse]


class OrderStatusUpdate(CamelModel):
    order_status: Optional[int] = Field(
        None,
        title="Order Status",
        description="The order status of your order for tracking order details",
    )
