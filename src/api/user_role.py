from fastapi import APIRouter, Depends, status, Request
from src.dao.db import get_db
from src.dto.user_role import UserRoleCreate, UserRoleResponse, UserRoleUpdate
from src.service.user_role_service import user_role_service
from src.api.common_endpoints import USER_ROLE
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.dto.common import Jsonbody
from src.middleware.logger import logger
from fastapi.encoders import jsonable_encoder

router = APIRouter(tags=["User Roles module"])


@router.get(USER_ROLE + "/{user_role_id}", response_model=UserRoleResponse)
async def get_single_user_role(
    user_role_id: int, request: Request, db_obj: AsyncSession = Depends(get_db)
):
    """
    This endpoint gets single user role details by their user role id
    """
    logger.info(f"Fetching user role with ID: {user_role_id}")
    result = await user_role_service.get_user_role_by_id(
        user_role_id=user_role_id, db_obj=db_obj
    )
    logger.info(
        f"User role details fetched successfully with the response: {jsonable_encoder(result)}"
    )
    return result


@router.post(USER_ROLE, response_model=UserRoleResponse)
async def create_new_user_role(
    user_role_create: UserRoleCreate, db_obj: AsyncSession = Depends(get_db)
):
    """
    This endpoint creates a new user role.
    """
    payload = user_role_create.dict()
    logger.info(
        f"Creating user role details for ID {user_role_create.id} with the payload: {payload}"
    )
    result = await user_role_service.create_user_role_details(
        user_role_create=user_role_create, db_obj=db_obj
    )
    logger.info(
        f"User role details created successfully for {user_role_create.id} with the response: {jsonable_encoder(result)}"
    )
    return result


@router.patch(USER_ROLE + "/{user_role_id}", response_model=UserRoleResponse)
async def update_existing_user(
    user_role_id: int, user_role: UserRoleUpdate, db_obj: AsyncSession = Depends(get_db)
):
    """
    This endpoint updates an existing user details in the database.
    """
    payload = user_role.dict()
    logger.info(
        f"Updating user role details for ID {user_role_id} with the payload: {payload}"
    )
    result = await user_role_service.update_existing_user_role(
        user_role_id, user_role, db_obj=db_obj
    )
    logger.info(
        f"User role details updated successfully for {user_role_id} with the response: {jsonable_encoder(result)}"
    )
    return result


@router.delete(USER_ROLE + "/{user_role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_user_role(
    user_role_id: int, db_obj: AsyncSession = Depends(get_db)
):
    """
    This endpoint deletes a user role by given id.
    """
    logger.info(f"Deleting user role details for ID: {user_role_id}")
    result = await user_role_service.delete_existing_user_role(
        user_role_id=user_role_id, db_obj=db_obj
    )
    logger.info(f"User role details deleted successfully.")
    return result


@router.get(USER_ROLE, response_model=List[UserRoleResponse])
async def all_users_role(
    json: Jsonbody = Depends(),
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint gets the user role from the database by applying filtering, searching and sorting.
    """
    logger.info("Fetching all user roles details.")
    result = await user_role_service.get_all_user_role(json=json, db_obj=db_obj)
    logger.info(
        f"All user role details fetched successfully with the response {jsonable_encoder(result)}"
    )
    return result
