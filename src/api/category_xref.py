from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from src.api.common_endpoints import SUBCATEGORY
from src.dao.db import get_db
from src.dto.subcategory import XrefSubcategoryResponse
from src.service.category_xref_service import category_xref_service
from src.middleware.logger import logger
from fastapi.encoders import jsonable_encoder

router = APIRouter(tags=["Category_Xref module"])


@router.get(
    SUBCATEGORY + "/{category_id}", response_model=List[XrefSubcategoryResponse]
)
async def get_all_subcategories_from_category_xref_by_category_id(
    category_id: UUID, db_obj: AsyncSession = Depends(get_db)
):
    """
    This endpoint gets single category details with their all subcategories by category id.
    """
    logger.info(
        f"Fetching single category details with their all subcategories by category id: {category_id}"
    )
    result = await category_xref_service.get_all_subcategories_by_category_id(
        category_id=category_id, db_obj=db_obj
    )
    logger.info(
        f"Category details annd their subcategory details fetched successfully from category xref with the response: {jsonable_encoder(result)}"
    )
    return result
