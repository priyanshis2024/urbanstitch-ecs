from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.api.common_endpoints import CATEGORY
from src.dao.db import get_db
from src.dto.category import (
    CategoryResponse,
    CategoryCreate,
    CategoryUpdate,
    Categorydetails,
    CategoryDetailListResponse,
    DeleteCategoryResponse,
    DeleteCategoryRequest,
    CategoryUpdateStatus,
    CategoryBulkResponse,
)
from src.service.category_service import category_service
from src.utils.utils import get_current_user
from typing import Optional, List
from src.dto.common import Jsonbody
from src.middleware.logger import logger
from fastapi.encoders import jsonable_encoder

router = APIRouter(tags=["Category module"])


@router.get(CATEGORY + "/{category_id}", response_model=Categorydetails)
async def get_category_by_id(category_id: UUID, db_obj: AsyncSession = Depends(get_db)):
    """
    This endpoint gets single category details by category id.
    """
    logger.info(f"Fetching category details with ID: {category_id}")
    result = await category_service.get_category_by_id(
        category_id=category_id, db_obj=db_obj
    )
    logger.info(
        f"Category details fetched successfully with the response: {jsonable_encoder(result)}"
    )
    return result


@router.get(
    CATEGORY + "/{category_id}" + "/subcategories", response_model=CategoryResponse
)
async def get_category_with_subcategory(
    category_id: UUID, db_obj: AsyncSession = Depends(get_db)
):
    """
    This endpoint fetches category details by category ID, including its subcategories.
    """
    logger.info(
        f"Fetching category and subcategory details with category ID: {category_id}"
    )
    result = await category_service.get_category_by_id_with_subcategory(
        category_id=category_id, db_obj=db_obj
    )
    logger.info(
        f"Category details annd their subcategory details fetched successfully with the response: {jsonable_encoder(result)}"
    )
    return result


@router.post(CATEGORY, response_model=CategoryResponse)
async def create_category(
    category: CategoryCreate,
    user_id: str = Depends(get_current_user),
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint creates new category and subcategory details in the database.
    """
    request_payload = category.dict()
    logger.info(f"Creating category details with the payload: {request_payload}")
    result = await category_service.create_category(
        category_create=category, user_id=user_id, db_obj=db_obj
    )
    logger.info(
        f"Category details created successfully for {result.id} with the response: {jsonable_encoder(result)}"
    )
    return result


@router.post(CATEGORY + "/bulk", response_model=CategoryBulkResponse)
async def create_bulk_categories(
    categories: List[CategoryCreate],
    user_id: str = Depends(get_current_user),
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint creates categories and their subcategories in bulk.
    """
    request_payload = categories.dict()
    logger.info(
        f"Creating category details in bulk with the payload: {request_payload}"
    )
    result = await category_service.create_bulk_categories(
        categories_create=categories, user_id=user_id, db_obj=db_obj
    )
    logger.info(
        f"All category details created successfully for {result.id} with the response: {jsonable_encoder(result)}"
    )
    return result


@router.patch(CATEGORY + "/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: UUID,
    category: CategoryUpdate,
    user_id: str = Depends(get_current_user),
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint updates an existing category and subcategory details in the database.
    """
    request_payload = category.dict()
    logger.info(
        f"Updating category details for ID {category_id} with the payload: {request_payload}"
    )
    result = await category_service.update_category(
        category_id=category_id,
        category_update=category,
        user_id=user_id,
        db_obj=db_obj,
    )
    logger.info(
        f"Category details updated successfully for {category_id} with the response: {jsonable_encoder(result)}"
    )
    return result


@router.delete(CATEGORY + "/{category_id}", response_model=DeleteCategoryResponse)
async def delete_category(
    category_id: UUID,
    request_body: Optional[DeleteCategoryRequest] = None,
    db_obj: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user),
):
    """
    API to delete a category or specific subcategories.

    - If no request body is provided, deletes the entire category along with unlinked subcategories.
    - If subcategories are specified in the request body, only those subcategories are deleted.
    """
    logger.info(f"Deleting category details for ID: {category_id}")
    result = await category_service.delete_category(
        category_id=category_id,
        user_id=user_id,
        db_obj=db_obj,
        request_body=request_body,
    )
    logger.info(f"Category details deleted successfully.")
    return result


@router.get(CATEGORY, response_model=CategoryDetailListResponse)
async def get_all_categories(
    json: Jsonbody = Depends(),
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint fetches categories by applying pagination, searching, and sorting.
    """
    logger.info("Fetching all category details.")
    result = await category_service.get_all_category(json=json, db_obj=db_obj)
    logger.info(
        f"All category details fetched successfully with the response {jsonable_encoder(result)}"
    )
    return result


@router.patch(CATEGORY + "/{category_id}" + "/status", response_model=Categorydetails)
async def change_category_status(
    category_id: UUID,
    category_update_status: CategoryUpdateStatus,
    db_obj: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    """
    This endpoint updates an existing category status in the database.
    """
    payload = category_update_status.dict()
    logger.info(
        f"Updating category status for ID {category_id} with the payload: {payload}"
    )
    result = await category_service.change_category_status(
        category_id=category_id,
        user_id=user_id,
        category_update_status=category_update_status,
        db_obj=db_obj,
    )
    logger.info(
        f"Category status updated successfully for {category_id} with the response {jsonable_encoder(result)}"
    )
    return result
