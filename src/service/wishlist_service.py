from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from uuid import UUID
from src.service.wishlist_converter import Converter
from src.dao.db import transaction
from uuid import UUID
from src.dao.models.product import Wishlist
from src.exceptions.wishlist import (
    WishlistProductAlreadyExists,
    WishlistNotFound,
)
from src.exceptions.user import UnauthorizedUser
from src.utils.user_id import ADMIN_USER_ID
from src.dao.wishlist import wishlist_dao
from src.dto.wishlist import WishlistCreate
from src.utils.constants import UuidPrefix
from src.utils.utils import attach_prefix_to_uuid
from src.dto.common import Json_pagination
from src.utils.constants import ErrorMessage
from src.middleware.logger import logger


class WishlistService:
    async def get_wishlist_by_id(self, wishlist_id: UUID, db_obj: AsyncSession):
        """
        Service function to get a wishlist by ID asynchronously.
        :param db_obj: The session object
        :param wishlist_id: The ID of the wishlist to retrieve
        :return: wishlist object or None
        """
        result = await wishlist_dao.get_wishlist_by_id(
            wishlist_id=wishlist_id, db_obj=db_obj
        )
        if not result:
            logger.error(f"Wishlist with id '{wishlist_id}' not found in the system.")
            raise WishlistNotFound(
                wishlist_id=wishlist_id,
                message=ErrorMessage.WISHLIST_NOT_FOUND.format(wishlist_id=wishlist_id),
            )
        return result

    @transaction
    async def create_wishlist_details(
        self, wishlist_create: WishlistCreate, user_id: UUID, db_obj: AsyncSession
    ):
        """
        Service function to create a new wishlist asynchronously.
        :param db_obj: The session object
        :param wishlist_create: The wishlist creation DTO
        :return: Created wishlist object (DTO)
        """

        if user_id == ADMIN_USER_ID:
            logger.error(
                f"Unauthorized user. User with id '{user_id}' is not authorized user to access this resource."
            )
            raise UnauthorizedUser(
                user_id=user_id,
                message=ErrorMessage.UNAUTHORIZED_USER.format(user_id=user_id),
            )

        temp_user = attach_prefix_to_uuid(
            input_uuid=user_id, prefix=UuidPrefix.USER.value
        )

        existing_product = await wishlist_dao.fetch_wishlist_product(
            db_obj=db_obj,
            subproduct_id=wishlist_create.subproduct_id,
            wishlist_id=Wishlist.id,
            user_id=temp_user,
        )
        if existing_product:
            logger.error(
                f"Wishlist with subproduct id '{wishlist_create.subproduct_id}' already exists in the system."
            )
            raise WishlistProductAlreadyExists(
                wishlist_id=Wishlist.id,
                message=ErrorMessage.WISHLIST_ALREADY_EXISTS.format(
                    subproduct_id=", ".join(wishlist_create.subproduct_id)
                ),
            )
        wishlist_db = Converter.wishlist_create_dto_to_db(wishlist_create)
        wishlist_db.user_id = temp_user
        wishlist_db = await wishlist_dao.create_wishlist(db_obj, wishlist_db)

        wishlist_details = await wishlist_dao.fetch_wishlist_with_details(
            db_obj=db_obj, wishlist_id=wishlist_db.id
        )

        return Converter.wishlist_detail_dto_to_db(wishlist_details)

    @transaction
    async def delete_existing_wishlist(
        self, wishlist_id: UUID, user_id: UUID, db_obj: AsyncSession
    ):
        """
        Service function to delete a wishlist asynchronously.
        :param db_obj: The session object
        :param wishlist_id: The ID of the wishlist to delete
        :return: Dictionary with success status
        """
        if user_id == ADMIN_USER_ID:
            logger.error(
                f"Unauthorized user. User with id '{user_id}' is not authorized user to access this resource."
            )
            raise UnauthorizedUser(
                user_id=user_id,
                message=ErrorMessage.UNAUTHORIZED_USER.format(user_id=user_id),
            )

        wishlist_db = await wishlist_dao.get_wishlist_by_id(
            wishlist_id=wishlist_id, db_obj=db_obj
        )
        if not wishlist_db:
            logger.error(f"Wishlist with id '{wishlist_id}' not found in the system.")
            raise WishlistNotFound(
                wishlist_id=wishlist_id,
                message=ErrorMessage.WISHLIST_NOT_FOUND.format(wishlist_id=wishlist_id),
            )
        await wishlist_dao.delete_wishlist(db_obj, wishlist_db)
        return {"status": "Success"}

    async def get_all_wishlist_details(
        self, json: Json_pagination, db_obj: AsyncSession, user_id: str
    ):
        """
        Service function to get all wishlist items for a user with pagination and search.
        """
        response = await wishlist_dao.get_all_wishlist_details(
            db_obj=db_obj,
            user_id=user_id,
            search=json.search,
            limit=json.limit,
            offset=json.offset,
        )

        return Converter.wishlist_detail_list_response_db_to_dto(response)


wishlist_service = WishlistService()
