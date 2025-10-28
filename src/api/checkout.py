from fastapi import APIRouter, Depends, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.api.common_endpoints import CART, CHECKOUT
from src.dao.db import get_db
from src.dto.checkout import (
    CartResponse,
    CartCreate,
    CartDetailResponse,
    CartUpdate,
    CartListDetailResponse,
    CheckoutSessionRequest,
    CheckoutSessionResponse,
)
from src.utils.utils import get_current_user
from src.service.checkout_service import cart_service
from src.dto.common import Jsonbody
from typing import Optional
from src.middleware.logger import logger
from fastapi.encoders import jsonable_encoder


router = APIRouter(tags=["Checkout module"])


@router.get(CART + "/{cart_id}", response_model=CartResponse)
async def get_cart_by_id(cart_id: UUID, db_obj: AsyncSession = Depends(get_db)):
    logger.info(f"Fetching cart details with ID: {cart_id}")
    result = await cart_service.get_cart_by_id(cart_id=cart_id, db_obj=db_obj)
    logger.info(
        f"Cart details fetched successfully with the response: {jsonable_encoder(result)}"
    )
    return result


@router.post(CART, response_model=CartDetailResponse)
async def create_cart(
    cart: CartCreate,
    user_id: str = Depends(get_current_user),
    db_obj: AsyncSession = Depends(get_db),
):
    request_payload = cart.dict()
    logger.info(f"Creating cart details with the payload: {request_payload}")
    result = await cart_service.create_cart_details(
        cart_create=cart, user_id=user_id, db_obj=db_obj
    )
    logger.info(
        f"Cart details created successfully for {result.id} with the response: {jsonable_encoder(result)}"
    )
    return result


@router.put(CART + "/{cart_id}", response_model=CartDetailResponse)
async def update_cart(
    cart_id: UUID,
    cart: CartUpdate,
    user_id: str = Depends(get_current_user),
    db_obj: AsyncSession = Depends(get_db),
):
    request_payload = cart.dict()
    logger.info(
        f"Updating cart details for ID {cart_id} with the payload: {request_payload}"
    )
    result = await cart_service.update_existing_cart(
        cart_id=cart_id, cart_update=cart, user_id=user_id, db_obj=db_obj
    )
    logger.info(
        f"Cart details updated successfully for {cart_id} with the response: {jsonable_encoder(result)}"
    )
    return result


@router.delete(CART, status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart(
    cart_id: Optional[UUID] = Header(None, alias="cart_id"),
    user_id: Optional[str] = Depends(get_current_user),
    db_obj: AsyncSession = Depends(get_db),
):
    logger.info(f"Deleting cart details for ID: {cart_id}")
    result = await cart_service.delete_existing_cart(
        cart_id=cart_id, user_id=user_id, db_obj=db_obj
    )
    logger.info(f"Cart details deleted successfully.")
    return result


@router.get(CART, response_model=CartListDetailResponse)
async def get_all_cart(
    json: Jsonbody = Depends(),
    db_obj: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    logger.info("Fetching all cart details.")
    result = await cart_service.get_all_cart(json=json, db_obj=db_obj, user_id=user_id)
    logger.info(
        f"All cart details fetched successfully with the response {jsonable_encoder(result)}"
    )
    return result


@router.post(CHECKOUT, response_model=CheckoutSessionResponse)
async def create_checkout_session(request: CheckoutSessionRequest):
    logger.info(f"Initializing checkout session API.")
    response = await cart_service.create_checkout_session(request)
    response_dict = response.dict()
    result = CheckoutSessionResponse(**response_dict)
    logger.info(
        f"Cart details created successfully for {result.id} with the response: {jsonable_encoder(result)}"
    )
    return result
