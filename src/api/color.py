from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.common_endpoints import COLOR
from src.dao.db import get_db
from src.dto.color import ColorResponse
from src.service.color_service import color_service
from uuid import UUID
from typing import Optional, List
from src.dto.common import Json_pagination
from fastapi.encoders import jsonable_encoder
from src.middleware.logger import logger

router = APIRouter(tags=["Colors module"])


@router.get(COLOR, response_model=ColorResponse)
async def get_all_distinct_colors(
    json: Json_pagination = Depends(),
    category_id: Optional[UUID] = None,
    subcategory_id: Optional[List[UUID]] = Query(None),
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint fetches colors by applying filters of category, subcategory, empty and both.
    """
    logger.info("Fetching all distinct colors.")
    result = await color_service.get_all_distinct_color(
        json=json, category_id=category_id, subcategory_id=subcategory_id, db_obj=db_obj
    )
    logger.info(
        f"All distinct colors fetched successfully with the response {jsonable_encoder(result)}"
    )
    return result
