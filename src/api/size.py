from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.utils.utils import get_current_user
from fastapi import Depends, status, APIRouter, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.common_endpoints import SIZE, SIZE_LIST
from src.dao.db import get_db
from src.dto.size import (
    SizeCreate,
    SizeListResponse,
    SizeUpdate,
    SizeResponse,
    SizeBulkResponse,
)
from src.service.size_service import size_service
from src.utils.utils import get_current_user
from typing import Optional, List
from src.dto.common import Jsonbody
from src.middleware.logger import logger
from fastapi.encoders import jsonable_encoder

router = APIRouter(tags=["Size module"])


@router.get(SIZE + "/{size_id}", response_model=SizeResponse)
async def get_size_by_id(size_id: UUID, db_obj: AsyncSession = Depends(get_db)):
    """
    This endpoint gets single size details by size id
    """
    logger.info(f"Fetching size details with ID: {size_id}")
    result = await size_service.get_size_by_id(size_id=size_id, db_obj=db_obj)
    logger.info(
        f"Size details fetched successfully with the response: {jsonable_encoder(result)}"
    )
    return result


@router.post(SIZE, response_model=SizeBulkResponse)
async def create_sizes(
    sizes: List[SizeCreate],
    user_id: str = Depends(get_current_user),
    db_obj: AsyncSession = Depends(get_db),
):
    """
    Bulk insert sizes.
    """
    request_payload = sizes.dict()
    logger.info(f"Creating size details with the payload: {request_payload}")
    result = await size_service.create_bulk_size_details(
        sizes_create=sizes, user_id=user_id, db_obj=db_obj
    )
    logger.info(
        f"Size details created successfully for {result.id} with the response: {jsonable_encoder(result)}"
    )
    return result


@router.patch(SIZE + "/{size_id}", response_model=SizeResponse)
async def update_size(
    size_id: UUID,
    size: SizeUpdate,
    user_id: str = Depends(get_current_user),
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint updates an existing size details in the database.
    """
    request_payload = size.dict()
    logger.info(
        f"Updating size details for ID {size_id} with the payload: {request_payload}"
    )
    result = await size_service.update_existing_size(
        size_id=size_id, size_update=size, user_id=user_id, db_obj=db_obj
    )
    logger.info(
        f"Size details updated successfully for {size_id} with the response: {jsonable_encoder(result)}"
    )
    return result


@router.delete(SIZE + "/{size_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_size(
    size_id: UUID,
    user_id: str = Depends(get_current_user),
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint deletes a size by given id.
    """
    logger.info(f"Deleting size details for ID: {size_id}")
    result = await size_service.delete_existing_size(
        size_id=size_id, user_id=user_id, db_obj=db_obj
    )
    logger.info(f"Size details deleted successfully.")
    return result


@router.get(SIZE_LIST, response_model=SizeListResponse)
async def get_all_sizes(
    json: Jsonbody = Depends(),
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint fetches sizes by applying pagination, searching, and sorting.
    """
    logger.info("Fetching all size details.")
    result = await size_service.get_all_size(json=json, db_obj=db_obj)
    logger.info(
        f"All size details fetched successfully with the response {jsonable_encoder(result)}"
    )
    return result


@router.get(SIZE, response_model=SizeListResponse)
async def get_all_distinct_sizes(
    json: Jsonbody = Depends(),
    category_id: Optional[UUID] = None,
    subcategory_id: Optional[List[UUID]] = Query(None),
    db_obj: AsyncSession = Depends(get_db),
):
    logger.info("Fetching all distinct size details.")
    result = await size_service.get_all_distinct_size(
        json=json, category_id=category_id, subcategory_id=subcategory_id, db_obj=db_obj
    )
    logger.info(
        f"All distinct size details fetched successfully with the response {jsonable_encoder(result)}"
    )
    return result
