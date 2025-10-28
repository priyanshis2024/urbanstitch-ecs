from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.api.common_endpoints import SUBPRODUCT
from src.dao.db import get_db
from src.dto.subproduct import (
    SubproductCreate,
    SubproductResponse,
    SubproductUpdate,
    SubproductUpdateStatus,
    SubproductDetailResponse,
    SubproductDetailListResponse,
    SubproductBulkResponse,
)
from src.service.subproduct_service import subproduct_service
from src.utils.utils import get_current_user
from src.dto.common import SubproductSearchPayload
from typing import List
from src.middleware.logger import logger
from fastapi.encoders import jsonable_encoder

router = APIRouter(tags=["Subproduct module"])


@router.post(
    SUBPRODUCT + "/search" + "/listing", response_model=SubproductDetailListResponse
)
async def get_all_subproducts_listing(
    payload: SubproductSearchPayload,
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint fetches subproducts by applying pagination, searching, and sorting.
    """
    logger.info("Fetching all subproduct details.")
    result = await subproduct_service.get_all_subproduct_with_product_detail(
        payload=payload, db_obj=db_obj
    )
    logger.info(
        f"All subproduct details fetched successfully with the response {jsonable_encoder(result)}"
    )
    return result


@router.get(
    SUBPRODUCT + "/product_details" + "/{subproduct_id}",
    response_model=SubproductDetailResponse,
)
async def get_subproduct_details_product(
    subproduct_id: UUID, db_obj: AsyncSession = Depends(get_db)
):
    """
    This endpoint get an existing subproduct details by their id from the database.
    """
    logger.info(f"Fetching subproduct details with ID: {subproduct_id}")
    result = await subproduct_service.get_single_subproduct_detail(
        subproduct_id=subproduct_id, db_obj=db_obj
    )
    logger.info(
        f"Subproduct details fetched successfully with the response: {jsonable_encoder(result)}"
    )
    return result


@router.post(SUBPRODUCT, response_model=SubproductBulkResponse)
async def create_subproduct(
    subproducts: List[SubproductCreate],
    user_id: str = Depends(get_current_user),
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint create an subproduct details in the database.
    """
    request_payload = subproducts.dict()
    logger.info(
        f"Creating subproduct details in bulk with the payload: {request_payload}"
    )
    result = await subproduct_service.create_bulk_subproduct(
        subproducts_create=subproducts, user_id=user_id, db_obj=db_obj
    )
    logger.info(
        f"All subproduct details created successfully for {result.id} with the response: {jsonable_encoder(result)}"
    )
    return result


@router.patch(SUBPRODUCT + "/{subproduct_id}", response_model=SubproductResponse)
async def update_subproduct(
    subproduct_id: UUID,
    subproduct: SubproductUpdate,
    user_id: str = Depends(get_current_user),
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint updates an existing subproduct details in the database.
    """
    request_payload = subproduct.dict()
    logger.info(
        f"Updating subproduct details for ID {subproduct_id} with the payload: {request_payload}"
    )
    result = await subproduct_service.update_existing_subproduct(
        subproduct_id=subproduct_id,
        subproduct_update=subproduct,
        user_id=user_id,
        db_obj=db_obj,
    )
    logger.info(
        f"Subproduct details updated successfully for {subproduct_id} with the response: {jsonable_encoder(result)}"
    )
    return result


@router.delete(SUBPRODUCT + "/{subproduct_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subproduct(
    subproduct_id: UUID,
    user_id: str = Depends(get_current_user),
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint to delete a subproduct.
    """
    logger.info(f"Deleting subproduct details for ID: {subproduct_id}")
    result = await subproduct_service.delete_existing_subproduct(
        subproduct_id=subproduct_id, user_id=user_id, db_obj=db_obj
    )
    logger.info(f"Subproduct details deleted successfully.")
    return result


@router.patch(
    SUBPRODUCT + "/{subproduct_id}" + "/status", response_model=SubproductResponse
)
async def change_subproduct_status(
    subproduct_id: UUID,
    subproduct_update_status: SubproductUpdateStatus,
    db_obj: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    """
    This endpoint updates an existing subproduct's status in the database.
    """
    payload = subproduct_update_status.dict()
    logger.info(
        f"Updating subproduct status for ID {subproduct_id} with the payload: {payload}"
    )
    result = await subproduct_service.change_subproduct_status(
        subproduct_id=subproduct_id,
        user_id=user_id,
        subproduct_update_status=subproduct_update_status,
        db_obj=db_obj,
    )
    logger.info(
        f"Subproduct status updated successfully for {subproduct_id} with the response {jsonable_encoder(result)}"
    )
    return result
