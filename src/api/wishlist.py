from fastapi import APIRouter, Depends, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.api.common_endpoints import WISHLIST
from src.dao.db import get_db
from src.dto.wishlist import (
    WishlistCreate,
    WishlistResponse,
    WishlistDetailResponse,
    WishlistListDetailResponse,
)
from src.utils.utils import get_current_user
from src.service.wishlist_service import wishlist_service
from src.dto.common import Json_pagination
from src.middleware.logger import logger
from fastapi.encoders import jsonable_encoder

router = APIRouter(tags=["Wishlist module"])


@router.get(WISHLIST + "/{wishlist_id}", response_model=WishlistResponse)
async def get_wishlist_by_id_endpoint(
    wishlist_id: UUID, db_obj: AsyncSession = Depends(get_db)
):
    logger.info(f"Fetching wishlist details with ID: {wishlist_id}")
    result = await wishlist_service.get_wishlist_by_id(
        wishlist_id=wishlist_id, db_obj=db_obj
    )
    logger.info(
        f"Wishlist details fetched successfully with the response: {jsonable_encoder(result)}"
    )
    return result


@router.post(WISHLIST, response_model=WishlistDetailResponse)
async def create_new_wishlist(
    wishlist: WishlistCreate,
    user_id: str = Depends(get_current_user),
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint creates a wishlist.
    """
    request_payload = wishlist.dict()
    logger.info(f"Creating wishlist details with the payload: {request_payload}")
    result = await wishlist_service.create_wishlist_details(
        wishlist_create=wishlist, user_id=user_id, db_obj=db_obj
    )
    logger.info(
        f"Wishlist details created successfully for {result.id} with the response: {jsonable_encoder(result)}"
    )
    return result


@router.delete(WISHLIST + "/{wishlist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_wishlist(
    wishlist_id: UUID,
    user_id: str = Depends(get_current_user),
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint deletes a wishlist by given id.
    """
    logger.info(f"Deleting wishlist details for ID: {wishlist_id}")
    result = await wishlist_service.delete_existing_wishlist(
        wishlist_id=wishlist_id, user_id=user_id, db_obj=db_obj
    )
    logger.info(f"Wishlist details deleted successfully.")
    return result


@router.get(WISHLIST, response_model=WishlistListDetailResponse)
async def get_all_wishlist(
    json: Json_pagination = Depends(),
    db_obj: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    """
    Retrieve all wishlist items for a specific user with pagination and search.
    """
    logger.info("Fetching all wishlist details.")
    result = await wishlist_service.get_all_wishlist_details(
        json=json, db_obj=db_obj, user_id=user_id
    )
    logger.info(
        f"All wishlist details fetched successfully with the response {jsonable_encoder(result)}"
    )
    return result
