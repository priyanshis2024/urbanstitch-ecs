from fastapi import APIRouter, Depends, status
from src.dao.db import get_db
from src.dto.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserUpdateStatus,
    UserListResponse,
    UserCreationResponse,
)
from src.service.user_service import user_service
from src.api.common_endpoints import USER
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from src.dto.common import Jsonbody
from src.middleware.logger import logger
from fastapi.encoders import jsonable_encoder

router = APIRouter(tags=["Users module"])


@router.get(USER + "/{user_id}", response_model=UserResponse)
async def get_single_user(user_id: UUID, db_obj: AsyncSession = Depends(get_db)):
    """
    This endpoint gets single user details by user id
    """
    logger.info(f"Fetching user details with ID: {user_id}")
    result = await user_service.get_user_by_id(user_id=user_id, db_obj=db_obj)
    logger.info(
        f"User details fetched successfully with the response: {jsonable_encoder(result)}"
    )
    return result


@router.post(USER, response_model=UserCreationResponse)
async def create_new_user(
    user_create: UserCreate, db_obj: AsyncSession = Depends(get_db)
):
    """
    This endpoint creates a new user.
    """
    request_payload = user_create.dict()
    logger.info(f"Creating user details with the payload: {request_payload}")
    result = await user_service.create_user_details(user_create, db_obj=db_obj)
    logger.info(
        f"User details created successfully for {result.id} with the response: {jsonable_encoder(result)}"
    )
    return result


@router.patch(USER + "/{user_id}", response_model=UserResponse)
async def update_existing_user(
    user_id: UUID, user_update: UserUpdate, db_obj: AsyncSession = Depends(get_db)
):
    """
    This endpoint updates an existing user details in the database.
    """
    request_payload = user_update.dict()
    logger.info(
        f"Updating user details for ID {user_id} with the payload: {request_payload}"
    )
    result = await user_service.update_existing_user(
        user_id, user_update, db_obj=db_obj
    )
    logger.info(
        f"User details updated successfully for {user_id} with the response: {jsonable_encoder(result)}"
    )
    return result


@router.delete(USER + "/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_user(user_id: UUID, db_obj: AsyncSession = Depends(get_db)):
    """
    This endpoint deletes a user by given id.
    """
    logger.info(f"Deleting user details for ID: {user_id}")
    result = await user_service.delete_existing_user(user_id, db_obj=db_obj)
    logger.info(f"User details deleted successfully.")
    return result


@router.get(USER, response_model=UserListResponse)
async def all_users(json: Jsonbody = Depends(), db_obj: AsyncSession = Depends(get_db)):
    """
    This endpoint fetches users by applying pagination, searching, and sorting.
    """
    logger.info("Fetching all user details.")
    result = await user_service.get_all_users(json=json, db_obj=db_obj)
    logger.info(
        f"All user details fetched successfully with the response {jsonable_encoder(result)}"
    )
    return result


@router.patch(USER + "/{user_id}" + "/status", response_model=UserResponse)
async def change_user_status(
    user_id: UUID,
    user_update_status: UserUpdateStatus,
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint updates an existing user's status in the database.
    """
    payload = user_update_status.dict()
    logger.info(f"Updating user status for ID {user_id} with the payload: {payload}")
    result = await user_service.change_user_status(
        user_id=user_id, user_update_status=user_update_status, db_obj=db_obj
    )
    logger.info(
        f"User status updated successfully for {user_id} with the response {jsonable_encoder(result)}"
    )
    return result
