from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.service.review_converter import Converter
from src.dao.db import transaction
from src.dto.review import ReviewCreate, ReviewUpdate
from src.dao.reviews import review_dao
from src.utils.user_id import ADMIN_USER_ID
from src.exceptions.user import UnauthorizedUser
from src.exceptions.review import ReviewNotFound
from src.service.product_service import product_service
from src.utils.utils import attach_prefix_to_uuid
from src.utils.constants import UuidPrefix
from src.dto.common import Json_pagination
from src.utils.constants import ErrorMessage
from src.middleware.logger import logger


class ReviewService:
    async def get_review_by_id(self, review_id: UUID, db_obj: AsyncSession):
        """
        Service function to get a review by ID asynchronously.
        :param db_obj: The session object
        :param review_id: The ID of the review to retrieve
        :return: review object or None
        """
        if not review_id:
            logger.error(f"Review with id '{review_id}' not found in the system.")
            raise ReviewNotFound(
                review_id=review_id,
                message=ErrorMessage.REVIEW_NOT_FOUND.format(review_id=review_id),
            )
        return await review_dao.get_review_by_id(review_id=review_id, db_obj=db_obj)

    @transaction
    async def create_review_details(
        self, review_create: ReviewCreate, user_id: UUID, db_obj: AsyncSession
    ):
        """
        Service function to create a new review asynchronously.
        :param db_obj: The session object
        :param review_create: The review creation DTO
        :return: Created review object (DTO)
        """
        if user_id == ADMIN_USER_ID:
            logger.error(
                f"Unauthorized user. User with id '{user_id}' is not authorized user to access this resource."
            )
            raise UnauthorizedUser(
                user_id=user_id,
                message=ErrorMessage.UNAUTHORIZED_USER.format(user_id=user_id),
            )
        demo_user = attach_prefix_to_uuid(
            input_uuid=user_id, prefix=UuidPrefix.USER.value
        )

        review_db = Converter.review_create_dto_to_db(review_create)
        review_db.user_id = demo_user
        review_db.is_rated = (
            1 if review_create.rating is not None and review_create.rating > 0 else None
        )

        review = await review_dao.create_review(db_obj, review_db)
        await product_service.update_product_rating(
            review_create.product_id, db_obj=db_obj
        )
        return Converter.review_db_to_dto(review)

    @transaction
    async def update_existing_review(
        self,
        review_id: UUID,
        review_update: ReviewUpdate,
        user_id: UUID,
        db_obj: AsyncSession,
    ):
        """
        Service function to update an existing review asynchronously.
        :param db_obj: The session object
        :param review_id: The ID of the review to update
        :param review_update: The review update DTO
        :return: Updated review object (DTO) or None
        """
        if user_id == ADMIN_USER_ID:
            logger.error(
                f"Unauthorized user. User with id '{user_id}' is not authorized user to access this resource."
            )
            raise UnauthorizedUser(
                user_id=user_id,
                message=ErrorMessage.UNAUTHORIZED_USER.format(user_id=user_id),
            )

        demo_user = attach_prefix_to_uuid(
            input_uuid=user_id, prefix=UuidPrefix.USER.value
        )

        review_db = await review_dao.get_review_by_id(
            review_id=review_id, db_obj=db_obj
        )
        review_db.updated_by = demo_user
        if not review_db:
            logger.error(f"Review with id '{review_id}' not found in the system.")
            raise ReviewNotFound(
                review_id=review_id,
                message=ErrorMessage.REVIEW_NOT_FOUND.format(review_id=review_id),
            )
        product_id = review_db.product_id

        update_review = Converter.review_update_dto_to_db(review_update, review_db)

        updated_review = await review_dao.update_review(
            db_obj, update_review, review_update
        )
        await product_service.update_product_rating(
            product_id=product_id, db_obj=db_obj
        )
        return Converter.review_db_to_dto(updated_review)

    @transaction
    async def delete_existing_review(
        self, review_id: UUID, user_id: UUID, db_obj: AsyncSession
    ):
        """
        Service function to delete a review asynchronously.
        """
        if user_id == ADMIN_USER_ID:
            logger.error(
                f"Unauthorized user. User with id '{user_id}' is not authorized user to access this resource."
            )
            raise UnauthorizedUser(
                user_id=user_id,
                message=ErrorMessage.UNAUTHORIZED_USER.format(user_id=user_id),
            )

        review_db = await review_dao.get_review_by_id(
            review_id=review_id, db_obj=db_obj
        )

        if not review_db:
            logger.error(f"Review with id '{review_id}' not found in the system.")
            raise ReviewNotFound(
                review_id=review_id,
                message=ErrorMessage.REVIEW_NOT_FOUND.format(review_id=review_id),
            )
        product_id = review_db.product_id

        await review_dao.delete_review(db_obj, review_db)
        await product_service.update_product_rating(
            product_id=product_id, db_obj=db_obj
        )

        return {"status": "Success"}

    async def get_all_review(
        self, db_obj: AsyncSession, json: Json_pagination, product_id: UUID
    ):
        """
        Service function to fetch review asynchronously.
        :param: db_obj: The Async session object
        :param: payload: The search payload
        """
        response = await review_dao.all_review(
            db_obj=db_obj,
            search=json.search,
            limit=json.limit,
            offset=json.offset,
            product_id=product_id,
        )
        return Converter.review_response_db_to_dto(response)


review_service = ReviewService()
