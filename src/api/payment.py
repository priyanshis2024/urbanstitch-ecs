from src.api.common_endpoints import PAYMENT
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.dao.db import get_db
from src.service.payment_service import payment_service
from src.dto.payment import (
    PaymentCreate,
    PaymentResponse,
    PaymentStatusUpdate,
)
from src.utils.utils import get_current_user
from typing import List
from src.middleware.logger import logger
from fastapi.encoders import jsonable_encoder


router = APIRouter(tags=["Payment module"])


@router.post(PAYMENT, response_model=PaymentResponse)
async def create_payment(
    payment_create: PaymentCreate,
    db_obj: AsyncSession = Depends(get_db),
):
    """
    Create a payment for a given order.
    If the amount is not provided, it will be set as the order total price and status = PENDING.
    If the amount is provided and matches the order total price, status = SUCCESS.
    """
    request_payload = payment_create.dict()
    logger.info(f"Creating payment details with the payload: {request_payload}")
    result = await payment_service.create_payment(
        payment_create=payment_create, db_obj=db_obj
    )
    logger.info(
        f"Payment details created successfully for {result.id} with the response: {jsonable_encoder(result)}"
    )
    return result


@router.get(PAYMENT + "/{payment_id}", response_model=PaymentResponse)
async def get_payment_by_id(payment_id: UUID, db_obj: AsyncSession = Depends(get_db)):
    logger.info(f"Fetching payment details with ID: {payment_id}")
    result = await payment_service.get_payment_by_id(
        payment_id=payment_id, db_obj=db_obj
    )
    logger.info(
        f"Payment details fetched successfully with the response: {jsonable_encoder(result)}"
    )
    return result


@router.delete(PAYMENT + "/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payment(
    payment_id: UUID,
    user_id: str = Depends(get_current_user),
    db_obj: AsyncSession = Depends(get_db),
):
    logger.info(f"Deleting payment details for ID: {payment_id}")
    result = await payment_service.delete_payment(
        payment_id=payment_id, user_id=user_id, db_obj=db_obj
    )
    logger.info(f"Payment details deleted successfully.")
    return result


@router.get(PAYMENT, response_model=List[PaymentResponse])
async def get_all_payment(db_obj: AsyncSession = Depends(get_db)):
    logger.info("Fetching all payment details.")
    result = await payment_service.get_all_payment(db_obj=db_obj)
    logger.info(
        f"All payment details fetched successfully with the response {jsonable_encoder(result)}"
    )
    return result


@router.patch(PAYMENT + "/{payment_id}", response_model=PaymentResponse)
async def update_payment_details(
    payment_id: UUID,
    payment_update_status: PaymentStatusUpdate,
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint updates an existing payment's status and add the transaction ID in the database.
    """
    payload = payment_update_status.dict()
    logger.info(
        f"Updating payment status and adding transaction ID for the payment ID {payment_id} with the payload: {payload}"
    )
    result = await payment_service.update_payment_details(
        db_obj=db_obj,
        payment_id=payment_id,
        payment_update_status=payment_update_status,
    )
    logger.info(
        f"Payment status updated and transaction ID added successfully for the payment ID{payment_id} with the response {jsonable_encoder(result)}"
    )
    return result
