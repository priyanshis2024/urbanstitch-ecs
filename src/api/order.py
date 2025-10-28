from fastapi import APIRouter, Depends, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.api.common_endpoints import ORDER
from src.dao.db import get_db
from src.service.order_service import order_service
from src.dto.order import (
    UserOrderResponse,
    UserOrderCreationResponse,
    OrderResponse,
    UserOrderSummaryResponse,
    OrderSummaryResponse,
)
from src.utils.utils import get_current_user
from typing import Optional, Union
from src.dto.common import Json_pagination
from src.middleware.logger import logger
from fastapi.encoders import jsonable_encoder
from src.dao.models.product import Order

router = APIRouter(tags=["Order module"])


@router.post(ORDER, response_model=UserOrderCreationResponse)
async def create_order(
    user_id: str = Depends(get_current_user),
    customer_id: str = Header(None, convert_underscores=False),
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This API endpoint creates new order.
    Here user_id and customer_id are passed in the header.
    :user_id: The ID of the user creating the order
    :customer_id: The ID of the customer for whom the order is being created.
    :db_obj: The database session object
    """
    logger.info(f"Creating order details for the user's ID: {user_id}")
    result = await order_service.create_order(
        user_id=user_id, customer_id=customer_id, db_obj=db_obj
    )
    logger.info(
        f"Order details created successfully for {Order.id} with the response: {jsonable_encoder(result)}"
    )
    return result


@router.get(
    ORDER,
    response_model=Union[
        list[UserOrderResponse],  # user order details
        UserOrderSummaryResponse,  # admin user order summary
        OrderSummaryResponse,  # order summary
    ],
)
async def get_order_details(
    order_id: Optional[UUID] = None,
    user_id: Optional[UUID] = None,
    json: Json_pagination = Depends(),
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This API will handles to fetch order details from the database.
    order_id: If order id then fetch the order details for that order.
    user_id: If user id then fetch the order details for that user.
    json: JSON payload for the pagination
    db_obj: The database session object
    """
    if order_id:
        logger.info(f"Fetching order details with order ID: {order_id}")
        result = await order_service.get_order_details_by_order_id(
            order_id=order_id, db_obj=db_obj
        )
        logger.info(
            f"Order details fetched successfully with the response: {jsonable_encoder(result)}"
        )
        return result
    elif user_id:
        logger.info(f"Fetching order details with user ID: {user_id}")
        result = await order_service.get_all_orders_by_user_id(
            user_id=user_id, db_obj=db_obj
        )
        logger.info(
            f"Order details fetched successfully with the response: {jsonable_encoder(result)}"
        )
        return result
    else:
        logger.info("Fetching all order details.")
        result = await order_service.get_all_orders(json=json, db_obj=db_obj)
        logger.info(
            f"All order details fetched successfully with the response {jsonable_encoder(result)}"
        )
        return result


@router.patch(ORDER + "/{order_id}", response_model=OrderResponse)
async def cancel_order_and_manage_quantity(
    order_id: UUID,
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This API endpoint cancels an existing order and manages the quantity of the product.
    :order_id: UUID of the order to be cancelled.
    :db_obj: The database session object
    :return: The updated order details after cancellation.
    """
    logger.info(f"Order cancellation for order ID: {order_id}")
    result = await order_service.cancel_order(order_id=order_id, db_obj=db_obj)
    logger.info(
        f"Order for the id {order_id} is cancelled. Response: {jsonable_encoder(result)}"
    )
    return result


@router.delete(ORDER + "/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(id: UUID, db_obj: AsyncSession = Depends(get_db)):
    logger.info(f"Deleting order details for ID: {id}")
    result = await order_service.delete_order(id=id, db_obj=db_obj)
    logger.info(f"Order details deleted successfully.")
    return result
