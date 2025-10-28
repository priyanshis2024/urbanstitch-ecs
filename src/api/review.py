from fastapi import APIRouter, Depends, status, Header
from src.dao.db import get_db
from src.dto.review import (
    ReviewCreate,
    ReviewResponse,
    ReviewUpdate,
    ReviewListResponse,
)
from src.service.review_service import review_service
from src.api.common_endpoints import REVIEW
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.utils import get_current_user
from src.dto.common import Json_pagination
from src.middleware.logger import logger
from fastapi.encoders import jsonable_encoder

router = APIRouter(tags=["Reviews module"])


@router.get(REVIEW + "/{review_id}", response_model=ReviewResponse)
async def get_single_review(review_id: UUID, db_obj: AsyncSession = Depends(get_db)):
    """
    This endpoint gets single review details by their review id
    """
    logger.info(f"Fetching review details with ID: {review_id}")
    result = await review_service.get_review_by_id(review_id=review_id, db_obj=db_obj)
    logger.info(
        f"Review details fetched successfully with the response: {jsonable_encoder(result)}"
    )
    return result


@router.post(REVIEW, response_model=ReviewResponse)
async def create_new_review(
    review: ReviewCreate,
    user_id: str = Depends(get_current_user),
    db_obj: AsyncSession = Depends(get_db),
):
    """
    This endpoint creates a new review.
    """
    request_payload = review.dict()
    logger.info(f"Creating review details with the payload: {request_payload}")
    result = await review_service.create_review_details(
        review_create=review, user_id=user_id, db_obj=db_obj
    )
    logger.info(
        f"Review details created successfully for {result.id} with the response: {jsonable_encoder(result)}"
    )
    return result


@router.put(REVIEW + "/{review_id}", response_model=ReviewResponse)
async def update_existing_review(
    review_id: UUID, review: ReviewUpdate, db_obj: AsyncSession = Depends(get_db)
):
    """
    This endpoint updates an existing review details in the database.
    """
    request_payload = review.dict()
    logger.info(
        f"Updating review details for ID {review_id} with the payload: {request_payload}"
    )
    result = await review_service.update_existing_review(
        review_id=review_id, review_update=review, db_obj=db_obj
    )
    logger.info(
        f"Review details updated successfully for {review_id} with the response: {jsonable_encoder(result)}"
    )
    return result


@router.delete(REVIEW + "/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_review(
    review_id: UUID, db_obj: AsyncSession = Depends(get_db)
):
    """
    This endpoint deletes a review by given id.
    """
    logger.info(f"Deleting review details for ID: {review_id}")
    result = await review_service.delete_existing_review(
        review_id=review_id, db_obj=db_obj
    )
    logger.info(f"Review details deleted successfully.")
    return result


@router.get(REVIEW, response_model=ReviewListResponse)
async def get_all_review(
    db_obj: AsyncSession = Depends(get_db),
    json: Json_pagination = Depends(),
    product_id: UUID = Header(None, alias="product_id"),
):
    """
    This endpoint gets the review from the database by applying filtering, searching and sorting.
    """
    logger.info("Fetching all review details.")
    result = await review_service.get_all_review(
        db_obj=db_obj, json=json, product_id=product_id
    )
    logger.info(
        f"All review details fetched successfully with the response {jsonable_encoder(result)}"
    )
    return result
