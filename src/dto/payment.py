"""This module handles request body, response body and field validation"""

from typing import Optional
from fastapi_camelcase import CamelModel
from pydantic import Field
from uuid import UUID
from datetime import datetime


class PaymentCreate(CamelModel):
    order_id: UUID = Field(
        ..., title="Order ID", description="The unique identifier of order"
    )
    amount: float = Field(
        ..., title="Amount", description="The payable amount of your order"
    )
    payment_status: int = Field(
        ...,
        title="Payment Status",
        description="The payment status of your order for tracking payments",
    )
    payment_method: Optional[int] = Field(
        None, title="Payment method", description="This is the payment method type."
    )
    transaction_id: Optional[str] = Field(
        None,
        title="Transaction id",
        description="This transaction id is stripe payment transaction id.",
    )


class PaymentResponse(CamelModel):
    id: UUID = Field(
        ..., title="ID", description="The unique identifier of the payment"
    )
    order_id: UUID = Field(
        ..., title="Order ID", description="The unique identifier of order"
    )
    amount: float = Field(
        ..., title="Amount", description="The payable amount of your order"
    )
    payment_status: int = Field(
        ...,
        title="Payment Status",
        description="The payment status of your order for tracking payments",
    )
    payment_method: int = Field(
        ..., title="Payment method", description="This is the payment method type."
    )
    transaction_id: Optional[str] = Field(
        None,
        title="Transaction id",
        description="This transaction id is stripe payment transaction id.",
    )
    refund_id: Optional[str] = Field(
        None,
        title="Refund id",
        description="This refund id is stripe payment refund id on the basis of the order cancellation.",
    )
    payment_at: Optional[datetime] = Field(
        None,
        title="Payement At",
        description="The timestamp when the payment details were created",
    )

    class Config:
        orm_mode = True


class PaymentStatusUpdate(CamelModel):
    payment_status: int = Field(
        ...,
        title="Payment Status",
        description="The payment status of your order for tracking payment details",
    )
    transaction_id: Optional[str] = Field(
        None,
        title="Transaction id",
        description="This transaction id is stripe payment transaction id.",
    )


class PaymentRefundUpdate(CamelModel):
    payment_status: int = Field(
        ...,
        title="Payment Status",
        description="The payment status of your order for tracking payment details",
    )
    refund_id: str = Field(
        ...,
        title="Refund id",
        description="This refund id is stripe payment refund id on the basis of the order cancellation.",
    )
