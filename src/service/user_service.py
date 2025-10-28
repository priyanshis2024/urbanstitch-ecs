from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.service.user_converter import Converter
from src.dao.db import transaction
from src.dto.user import UserCreate, UserUpdate, UserUpdateStatus
from src.exceptions.user import UserNotFound
from src.dao.users import user_dao
from src.dto.common import Jsonbody
from src.utils.constants import ErrorMessage
from src.middleware.logger import logger
from src.utils.utils import generate_password_hash, decrypt_password


class UserService:
    async def get_user_by_id(self, user_id: UUID, db_obj: AsyncSession):
        """
        Service function to get a user by ID asynchronously.
        :param db_obj: The session object
        :param user_id: The ID of the user to retrieve
        :return: User object or None
        """
        result = await user_dao.get_user(user_id=user_id, db_obj=db_obj)
        if not result:
            logger.error(f"User info with user id '{user_id}' not found in the system.")
            raise UserNotFound(
                user_id=user_id,
                message=ErrorMessage.USER_NOT_FOUND.format(user_id=user_id),
            )
        return result

    @transaction
    async def create_user_details(self, user_create: UserCreate, db_obj: AsyncSession):
        existing_user = await user_dao.fetch_email_detail(
            db_obj=db_obj, email=user_create.email
        )
        if existing_user:
            return Converter.user_creation_response_db_to_dto(
                existing_user, is_user_created=False
            )

        decrypted_password = decrypt_password(
            encrypted_password=user_create.password,
            encrypted_aes_key=user_create.encrypted_aes_key,
            iv=user_create.encrypted_aes_iv,
        )

        user_create.password = generate_password_hash(decrypted_password)

        user_db = Converter.user_create_dto_to_db(user_create)
        user = await user_dao.create_user(db_obj, user_db)
        return Converter.user_creation_response_db_to_dto(user, is_user_created=True)

    @transaction
    async def update_existing_user(
        self, user_id: UUID, user_update: UserUpdate, db_obj: AsyncSession
    ):
        """
        Service function to update an existing user asynchronously.
        :param db_obj: The session object
        :param user_id: The ID of the user to update
        :param user_update: The user update DTO
        :return: Updated User object (DTO) or None
        """
        user_db = await user_dao.get_user(user_id, db_obj)
        if not user_db:
            logger.error(f"User info with user id '{user_id}' not found in the system.")
            raise UserNotFound(
                user_id=user_id,
                message=ErrorMessage.USER_NOT_FOUND.format(user_id=user_id),
            )
        update_user = Converter.user_update_dto_to_db(user_update, user_db)
        updated_user = await user_dao.update_user(db_obj, update_user, user_update)
        return Converter.user_db_to_dto(updated_user)

    @transaction
    async def delete_existing_user(self, user_id: UUID, db_obj: AsyncSession):
        """
        Service function to delete a user asynchronously.
        :param db_obj: The session object
        :param user_id: The ID of the user to delete
        :return: Dictionary with success status
        """
        user_db = await user_dao.get_user(user_id, db_obj)
        if not user_db:
            logger.error(f"User info with user id '{user_id}' not found in the system.")
            raise UserNotFound(
                user_id=user_id,
                message=ErrorMessage.USER_NOT_FOUND.format(user_id=user_id),
            )
        await user_dao.delete_user(db_obj, user_db)
        return {"status": "Success"}

    async def get_all_users(self, db_obj: AsyncSession, json: Jsonbody):
        """
        Service function to fetch user role asynchronously.
        :param: db_obj: The Async session object
        :param: json: The json payload
        """
        response = await user_dao.all_user(
            db_obj=db_obj,
            search=json.search,
            limit=json.limit,
            offset=json.offset,
            sort_by=json.sort_by,
            sort_order=json.sort_order,
        )
        return Converter.user_response_db_to_dto(response)

    @transaction
    async def change_user_status(
        self, db_obj: AsyncSession, user_id: UUID, user_update_status: UserUpdateStatus
    ):
        """
        Service function to change the status of a user asynchronously.
        :param db_obj: The session object
        :param user_id: The ID of the user to update
        :param user_update_status: The status update schema from user dto
        :return: Updated status of the user
        """
        user_db = await user_dao.get_user(user_id, db_obj)
        if not user_db:
            logger.error(f"User info with user id '{user_id}' not found in the system.")
            raise UserNotFound(
                user_id=user_id,
                message=ErrorMessage.USER_NOT_FOUND.format(user_id=user_id),
            )
        updated_user = await user_dao.update_status(
            db_obj, user_db, user_update_status.status
        )
        return Converter.user_db_to_dto(updated_user)


user_service = UserService()
