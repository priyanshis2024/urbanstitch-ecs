from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.service.subcategory_converter import Converter
from src.dto.subcategory import SubcategoryUpdateStatus
from src.dao.db import transaction
from src.dao.subcategory import subcategory_dao
from src.exceptions.subcategory import SubcategoryNotFound
from src.utils.user_id import ADMIN_USER_ID
from src.exceptions.user import UnauthorizedUser
from src.dto.common import Jsonbody
from src.utils.constants import UuidPrefix
from src.utils.utils import attach_prefix_to_uuid
from src.utils.constants import ErrorMessage
from src.middleware.logger import logger


class SubcategoryService:
    @transaction
    async def change_subcategory_status(
        self,
        db_obj: AsyncSession,
        subcategory_id: UUID,
        user_id: UUID,
        subcategory_update_status: SubcategoryUpdateStatus,
    ):
        """
        Service function to change the status of a subcategory asynchronously.
        :param db_obj: The session object
        :param subcategory_id: The ID of the subcategory to update
        :param subcategory_update_status: The status update schema from subcategory dto
        :return: Updated status of the subcategory
        """
        if user_id != ADMIN_USER_ID:
            logger.error(
                f"Unauthorized user. User with id '{user_id}' is not authorized user to access this resource."
            )
            raise UnauthorizedUser(
                user_id=user_id,
                message=ErrorMessage.UNAUTHORIZED_USER.format(user_id=user_id),
            )
        admin_user = attach_prefix_to_uuid(
            input_uuid=user_id, prefix=UuidPrefix.USER.value
        )

        subcategory_db = await subcategory_dao.get_subcategory_by_id(
            subcategory_id, db_obj
        )
        if not subcategory_db:
            logger.error(
                f"Subcategory with id '{subcategory_id}' not found in the system."
            )
            raise SubcategoryNotFound(
                subcategory_id=subcategory_id,
                message=ErrorMessage.SUBCATEGORY_NOT_FOUND.format(
                    subcategory_id=subcategory_id
                ),
            )

        subcategory_db.updated_by = admin_user
        updated_subcategory = await subcategory_dao.update_subcategory_status(
            db_obj, subcategory_db, subcategory_update_status.status
        )
        return Converter.subcategory_db_to_dto(updated_subcategory)

    async def get_all_subcategory(self, json: Jsonbody, db_obj: AsyncSession):
        """
        Service function to fetch subcategories asynchronously.
        """
        response = await subcategory_dao.all_subcategory(
            db_obj=db_obj,
            search=json.search,
            sort_by=json.sort_by,
            sort_order=json.sort_order,
            limit=json.limit,
            offset=json.offset,
        )
        return Converter.subcategory_response_db_to_dto(response)


subcategory_service = SubcategoryService()
