from fastapi import APIRouter, Depends, status
from src.dao.db import get_db
from src.dto.contact_us import ContactUsCreate, ContactUsResponse, ContactUsUpdate
from src.service.contact_us_service import contact_us_service
from src.api.common_endpoints import CONTACT_US
from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.dto.common import Jsonbody
from src.middleware.logger import logger
from fastapi.encoders import jsonable_encoder

router = APIRouter(tags=["Contact us module"])


@router.get(CONTACT_US + "/{contact_us_id}", response_model=ContactUsResponse)
async def get_single_contact_us_details(
    contact_us_id: UUID, db_obj: AsyncSession = Depends(get_db)
):
    """
    This endpoint gets single contact us details by their id
    """
    logger.info(f"Fetching contact us details with ID: {contact_us_id}")
    result = await contact_us_service.get_contact_us_by_id(
        contact_us_id=contact_us_id, db_obj=db_obj
    )
    logger.info(
        f"Contact us details fetched successfully with the response: {jsonable_encoder(result)}"
    )
    return result


@router.post(CONTACT_US, response_model=ContactUsResponse)
async def create_new_contact_us(
    contact_us: ContactUsCreate, db_obj: AsyncSession = Depends(get_db)
):
    """
    This endpoint creates a new contact us details.
    """
    request_payload = contact_us.dict()
    logger.info(f"Creating contact us details with the payload: {request_payload}")
    result = await contact_us_service.create_contact_us_details(
        contact_us_create=contact_us, db_obj=db_obj
    )
    logger.info(
        f"Contact us details created successfully for {result.id} with the response: {jsonable_encoder(result)}"
    )
    return result


@router.patch(CONTACT_US + "/{contact_us_id}", response_model=ContactUsResponse)
async def update_existing_contact_us(
    contact_us_id: UUID,
    contact_us_update: ContactUsUpdate,
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint updates an existing contact us details in the database.
    """
    request_payload = contact_us_update.dict()
    logger.info(
        f"Updating contact us details for ID {contact_us_id} with the payload: {request_payload}"
    )
    result = await contact_us_service.update_existing_contact_us(
        contact_us_id, contact_us_update, db_obj=db_obj
    )
    logger.info(
        f"Contact us details updated successfully for {contact_us_id} with the response: {jsonable_encoder(result)}"
    )
    return result


@router.delete(CONTACT_US + "/{contact_us_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_contact_us(
    contact_us_id: UUID, db_obj: AsyncSession = Depends(get_db)
):
    """
    This endpoint deletes an contact us by given id.
    """
    logger.info(f"Deleting contact us details for ID: {contact_us_id}")
    result = await contact_us_service.delete_existing_contact_us(
        contact_us_id=contact_us_id, db_obj=db_obj
    )
    logger.info(f"Contact us details deleted successfully.")
    return result


@router.get(CONTACT_US, response_model=List[ContactUsResponse])
async def all_contact_us_details(
    json: Jsonbody = Depends(),
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint gets the contact us details from the database by applying filtering, searching and sorting.
    """
    logger.info("Fetching all contact us details.")
    result = await contact_us_service.get_all_contact_us(json=json, db_obj=db_obj)
    logger.info(
        f"All contact us details fetched successfully with the response {jsonable_encoder(result)}"
    )
    return result
