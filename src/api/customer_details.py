from fastapi import APIRouter, Depends, status
from src.dao.db import get_db
from src.dto.customer_details import (
    CustomerDetailCreate,
    CustomerDetailResponse,
    CustomerDetailUpdate,
    CustomerDetailListResponse,
)
from src.service.customer_detail_service import customer_detail_service
from src.api.common_endpoints import CUSTOMER_DETAILS, USER
from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.dto.common import Jsonbody
from src.utils.utils import get_current_user
from src.middleware.logger import logger
from fastapi.encoders import jsonable_encoder

router = APIRouter(tags=["Customer Details module"])


@router.get(
    CUSTOMER_DETAILS + "/{customer_detail_id}", response_model=CustomerDetailResponse
)
async def get_single_customer_detail(
    customer_detail_id: UUID, db_obj: AsyncSession = Depends(get_db)
):
    """
    This endpoint gets single customer_detail by their id
    """
    logger.info(f"Fetching customer detail with ID: {customer_detail_id}")

    result = await customer_detail_service.get_customer_detail_by_id(
        customer_detail_id=customer_detail_id, db_obj=db_obj
    )
    logger.info(
        f"Customer details fetched successfully with the response: {jsonable_encoder(result)}"
    )
    return result


@router.post(CUSTOMER_DETAILS, response_model=CustomerDetailResponse)
async def create_new_customer_detail(
    customer_detail_create: CustomerDetailCreate,
    user_id: str = Depends(get_current_user),
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint creates a new customer_detail details.
    """
    request_payload = customer_detail_create.dict()
    logger.info(f"Creating customer details with the payload: {request_payload}")
    result = await customer_detail_service.create_customer_detail_details(
        customer_detail_create=customer_detail_create, user_id=user_id, db_obj=db_obj
    )
    logger.info(
        f"Customer details created successfully for {result.id} with the response: {jsonable_encoder(result)}"
    )
    return result


@router.patch(
    CUSTOMER_DETAILS + "/{customer_detail_id}", response_model=CustomerDetailResponse
)
async def update_existing_customer_detail(
    customer_detail_id: UUID,
    customer_detail_update: CustomerDetailUpdate,
    user_id: str = Depends(get_current_user),
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint updates an existing customer_detail details in the database.
    """
    request_payload = customer_detail_update.dict()
    logger.info(
        f"Updating customer details for ID {customer_detail_id} with the payload: {request_payload}"
    )
    result = await customer_detail_service.update_existing_customer_detail(
        customer_detail_id, customer_detail_update, user_id=user_id, db_obj=db_obj
    )
    logger.info(
        f"Customer details updated successfully for {customer_detail_id} with the response: {jsonable_encoder(result)}"
    )
    return result


@router.delete(
    CUSTOMER_DETAILS + "/{customer_detail_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_existing_customer_detail(
    customer_detail_id: UUID,
    user_id: str = Depends(get_current_user),
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint deletes an customer_detail by given id.
    """
    logger.info(f"Deleting customer details for ID: {customer_detail_id}")
    result = await customer_detail_service.delete_existing_customer_detail(
        customer_detail_id=customer_detail_id, user_id=user_id, db_obj=db_obj
    )
    logger.info(f"Customer details deleted successfully.")
    return result


@router.get(CUSTOMER_DETAILS, response_model=List[CustomerDetailResponse])
async def all_customer_detail(
    json: Jsonbody = Depends(),
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint gets the customer_detail from the database by applying filtering, searching and sorting.
    """
    logger.info("Fetching all customer details.")
    result = await customer_detail_service.get_all_customer_detail(
        json=json, db_obj=db_obj
    )
    logger.info(
        f"All customer details fetched successfully with the response {jsonable_encoder(result)}"
    )
    return result


@router.get(
    CUSTOMER_DETAILS + USER + "/{user_id}", response_model=CustomerDetailListResponse
)
async def get_customers_details_by_user_id(
    user_id: UUID,
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint gets the customers_details by user id.
    """
    logger.info(f"Fetching customers details by user ID: {user_id}")
    result = await customer_detail_service.get_customers_details_by_user_id(
        user_id=user_id, db_obj=db_obj
    )
    logger.info(
        f"Customers details fetched successfully with the response {jsonable_encoder(result)}"
    )
    return result
