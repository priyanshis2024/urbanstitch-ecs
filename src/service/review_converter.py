from src.dto.review import (
    ReviewCreate,
    ReviewResponse,
    ReviewUpdate,
    ReviewListResponse,
)
from src.dao.models.product import Review
from fastapi.encoders import jsonable_encoder


class Converter:
    def review_db_to_dto(review_response: ReviewResponse):
        """
        Convert a contact us database model to a ContactUsResponse DTO.
        :param review_response: ContactUsResponse database model
        :return: ContactUsResponse DTO
        """
        review_dict = jsonable_encoder(review_response)
        return ReviewResponse(**review_dict)

    def review_response_db_to_dto(review_response: ReviewListResponse):
        """
        Convert a review database model to a ReviewListResponse DTO.
        :param review_response: User database model
        :return: ReviewListResponse DTO
        """
        return ReviewListResponse(
            total_review_count=len(review_response["reviews"]),
            reviews=[
                Converter.review_db_to_dto(review)
                for review in review_response["reviews"]
            ],
        )

    def review_create_dto_to_db(review_create: ReviewCreate):
        """
        Convert a ContactUsCreate DTO to a contact us database model.
        :param review_create: ContactUsCreate DTO
        :return: contact us database model
        """
        return Review(
            product_id=review_create.product_id,
            rating=review_create.rating,
            review=review_create.review,
            image=review_create.image,
        )

    def review_update_dto_to_db(review_update: ReviewUpdate, review: Review):
        """
        Convert a ContactUsUpdate DTO to a Contact us database model (updating an existing contact us).
        :param review_update: ContactUsUpdate DTO
        :param review: Existing contact us database model
        :return: Updated Contact us database model
        """
        for key, value in review_update.model_dump(exclude_unset=True).items():
            setattr(review, key, value)
        return review
