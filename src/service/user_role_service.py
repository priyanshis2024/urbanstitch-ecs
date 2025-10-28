from sqlalchemy.ext.asyncio import AsyncSession
from src.service.user_converter import Converter
from src.dao.db import transaction
from src.dto.user_role import UserRoleCreate, UserRoleUpdate
from src.exceptions.userrole import InvalidUserRole, UserRoleExist, UserRoleNotFound
from src.dao.user_role import user_role_dao
from src.dto.user_role import UserRoleCreate, UserRoleUpdate
from src.dto.common import Jsonbody
from src.utils.constants import ErrorMessage
from src.middleware.logger import logger


class UserRoleService:
    async def get_user_role_by_id(self, user_role_id: int, db_obj: AsyncSession):
        """
        Service function to get a user role by ID asynchronously.
        :param db: The session object
        :param user_role_id: The ID of the user role to retrieve
        :return: User role object or None
        """
        result = await user_role_dao.get_user_role(
            user_role_id=user_role_id, db_obj=db_obj
        )
        if not result:
            logger.error(f"User role with id '{user_role_id}' not found in the system.")
            raise UserRoleNotFound(
                user_role_id=user_role_id,
                message=ErrorMessage.USER_ROLE_NOT_FOUND.format(
                    user_role_id=user_role_id
                ),
            )
        return result

    @transaction
    async def create_user_role_details(
        self, user_role_create: UserRoleCreate, db_obj: AsyncSession
    ):
        """
        Service function to create a new user role asynchronously.
        :param db: The session object
        :param user_role_create: The user role creation DTO
        :return: Created User role object (DTO)
        """
        if not (1 <= user_role_create.id <= 4):
            logger.error(
                f"Invalid user role id '{user_role_create.id}'. User role must be between the range."
            )
            raise InvalidUserRole(
                user_role_id=user_role_create.id,
                message=ErrorMessage.INVALID_USER_ROLE.format(
                    user_role_id=user_role_create.id
                ),
            )

        existing_role = await user_role_dao.get_user_role(
            user_role_id=user_role_create.id, db_obj=db_obj
        )

        if existing_role:
            logger.error(
                f"User role with id '{user_role_create.id}' already exists in the system."
            )
            raise UserRoleExist(
                user_role_id=user_role_create.id,
                message=ErrorMessage.USER_ROLE_ALREADY_EXISTS.format(
                    user_role_id=user_role_create.id
                ),
            )

        user_role_db = Converter.user_role_create_dto_to_db(user_role_create)
        user_role = await user_role_dao.create_user_role(db_obj, user_role_db)
        return Converter.user_role_db_to_dto(user_role)

    @transaction
    async def update_existing_user_role(
        self, user_role_id: int, user_role_update: UserRoleUpdate, db_obj: AsyncSession
    ):
        """
        Service function to update an existing user role asynchronously.
        :param db: The session object
        :param user_role_id: The ID of the user role to update
        :param user_role_update: The user role update DTO
        :return: Updated User role object (DTO) or None
        """
        user_role_db = await user_role_dao.get_user_role(user_role_id, db_obj)
        if not user_role_db:
            logger.error(f"User role with id '{user_role_id}' not found in the system.")
            raise UserRoleNotFound(
                user_role_id=user_role_id,
                message=ErrorMessage.USER_ROLE_NOT_FOUND.format(
                    user_role_id=user_role_id
                ),
            )
        update_user_role = Converter.user_role_update_dto_to_db(
            user_role_update, user_role_db
        )
        updated_user_role = await user_role_dao.update_user_role(
            db_obj, update_user_role, user_role_update
        )
        return Converter.user_role_db_to_dto(updated_user_role)

    async def delete_existing_user_role(self, user_role_id: int, db_obj: AsyncSession):
        """
        Service function to delete a user role asynchronously.
        :param db: The session object
        :param user_role_id: The ID of the user role to delete
        :return: Dictionary with success status
        """
        user_role_db = await user_role_dao.get_user_role(user_role_id, db_obj)
        if not user_role_db:
            logger.error(f"User role with id '{user_role_id}' not found in the system.")
            raise UserRoleNotFound(
                user_role_id=user_role_id,
                message=ErrorMessage.USER_ROLE_NOT_FOUND.format(
                    user_role_id=user_role_id
                ),
            )
        await user_role_dao.delete_user_role(db_obj, user_role_db)
        return {"status": "Success"}

    async def get_all_user_role(self, db_obj: AsyncSession, json: Jsonbody):
        """
        Service function to fetch user role asynchronously.
        :param: db_obj: The Async session object
        :param: json: The json payload
        """
        try:
            user_roles = await user_role_dao.all_user_role(
                db_obj=db_obj,
                search=json.search,
                sort_by=json.sort_by,
                sort_order=json.sort_order,
                limit=json.limit,
                offset=json.offset,
            )
            return [Converter.user_role_db_to_dto(role) for role in user_roles]
        except Exception as e:
            logger.error(f"Error while fetching user roles: {str(e)}")
            raise


user_role_service = UserRoleService()
