from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.api.common_endpoints import SUBCATEGORY
from src.dao.db import get_db
from src.dto.subcategory import (
    SubcategoryUpdateStatus,
    SubcategoryResponse,
    SubcategoryDetailListResponse,
)
from src.service.subcategory_service import subcategory_service
from src.utils.utils import get_current_user
from src.dto.common import Jsonbody
from src.middleware.logger import logger
from fastapi.encoders import jsonable_encoder

router = APIRouter(tags=["Subcategory module"])


@router.get(SUBCATEGORY, response_model=SubcategoryDetailListResponse)
async def get_all_subcategories(
    json: Jsonbody = Depends(),
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint fetches subcategories by applying pagination, searching, and sorting.
    """
    logger.info("Fetching all subcategory details.")
    result = await subcategory_service.get_all_subcategory(json=json, db_obj=db_obj)
    logger.info(
        f"All subcategory details fetched successfully with the response {jsonable_encoder(result)}"
    )
    return result


@router.patch(
    SUBCATEGORY + "/{subcategory_id}" + "/status", response_model=SubcategoryResponse
)
async def change_subcategory_status(
    subcategory_id: UUID,
    subcategory_update_status: SubcategoryUpdateStatus,
    db_obj: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    """
    This endpoint updates an existing subcategory status in the database.
    """
    payload = subcategory_update_status.dict()
    logger.info(
        f"Updating subcategory status for ID {subcategory_id} with the payload: {payload}"
    )
    result = await subcategory_service.change_subcategory_status(
        subcategory_id=subcategory_id,
        user_id=user_id,
        subcategory_update_status=subcategory_update_status,
        db_obj=db_obj,
    )
    logger.info(
        f"Subcategory status updated successfully for {subcategory_id} with the response {jsonable_encoder(result)}"
    )
    return result
