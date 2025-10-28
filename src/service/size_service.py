from src.service.size_converter import Converter
from src.dao.db import transaction
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.service.size_converter import Converter
from src.dto.size import (
    SizeCreate,
    SizeUpdate,
)
from src.dao.size import size_dao
from src.exceptions.user import UnauthorizedUser
from src.exceptions.size import (
    SizeNotFound,
    SizeAlreadyExists,
)
from src.utils.user_id import ADMIN_USER_ID
from src.utils.constants import UuidPrefix
from src.utils.utils import attach_prefix_to_uuid
from typing import Optional, List
from src.dto.common import Jsonbody
from src.utils.constants import ErrorMessage
from src.middleware.logger import logger


class SizeService:
    async def get_size_by_id(self, size_id: UUID, db_obj: AsyncSession):
        """
        Service function to get a size by ID asynchronously.
        :param db_obj: The session object
        :param size_id: The ID of the size to retrieve
        :return: size object or None
        """
        result = await size_dao.get_size_by_id(size_id=size_id, db_obj=db_obj)
        if not result:
            logger.error(f"Size with id '{size_id}' not found in the system.")
            raise SizeNotFound(
                size_id=size_id,
                message=ErrorMessage.SIZE_NOT_FOUND.format(size_id=size_id),
            )
        return result

    @transaction
    async def create_bulk_size_details(
        self, sizes_create: List[SizeCreate], user_id: UUID, db_obj: AsyncSession
    ):
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

        size_ids = [size.id for size in sizes_create]

        existing_sizes = await size_dao.get_sizes_by_ids(
            size_ids=size_ids, db_obj=db_obj
        )

        existing_ids = {s.id for s in existing_sizes}

        created_sizes = []
        created_size_ids = []
        existing_size_ids = []

        for size in sizes_create:
            if size.id not in existing_ids:
                size_db = Converter.size_create_dto_to_db(size)
                size_db.created_by = admin_user
                size_db.updated_by = admin_user
                created_sizes.append(size_db)
                created_size_ids.append(str(size.id))
            else:
                existing_size_ids.append(str(size.id))

        if not created_sizes:
            logger.error(
                f"Size with id '{existing_size_ids}' already exists in the system."
            )
            raise SizeAlreadyExists(
                size_id=existing_size_ids,
                message=ErrorMessage.SIZE_ALREADY_EXISTS.format(
                    size_id=", ".join(existing_size_ids)
                ),
            )

        sizes = await size_dao.create_sizes_bulk(db_obj=db_obj, sizes=created_sizes)

        return {
            "created_size_count": len(created_size_ids),
            "existing_size_count": len(existing_size_ids),
            "data": [Converter.size_db_to_dto(s) for s in sizes],
            "created_size_ids": created_size_ids,
            "existing_size_ids": existing_size_ids,
        }

    @transaction
    async def update_existing_size(
        self,
        size_id: UUID,
        size_update: SizeUpdate,
        user_id: UUID,
        db_obj: AsyncSession,
    ):
        """
        Service function to update an existing size asynchronously.
        :param db_obj: The session object
        :param size_id: The ID of the size to update
        :param size_update: The size update DTO
        :param user_id: The ID of the user performing the update
        :return: Updated size object (DTO) or None
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

        size_db = await size_dao.get_size_by_id(size_id=size_id, db_obj=db_obj)
        size_db.updated_by = admin_user
        if not size_db:
            logger.error(f"Size with id '{size_id}' not found in the system.")
            raise SizeNotFound(
                size_id=size_id,
                message=ErrorMessage.SIZE_NOT_FOUND.format(size_id=size_id),
            )
        update_size = Converter.size_update_dto_to_db(size_update, size_db)
        updated_size = await size_dao.update_size(db_obj, update_size, size_update)
        return Converter.size_db_to_dto(updated_size)

    @transaction
    async def delete_existing_size(
        self, size_id: UUID, user_id: UUID, db_obj: AsyncSession
    ):
        """
        Service function to delete a size asynchronously.
        :param db_obj: The session object
        :param size_id: The ID of the size to delete
        :param user_id: The ID of the user performing the size detail deletion
        :return: Dictionary with success status
        """
        if user_id != ADMIN_USER_ID:
            logger.error(
                f"Unauthorized user. User with id '{user_id}' is not authorized user to access this resource."
            )
            raise UnauthorizedUser(
                user_id=user_id,
                message=ErrorMessage.UNAUTHORIZED_USER.format(user_id=user_id),
            )
        size_db = await size_dao.get_size_by_id(size_id=size_id, db_obj=db_obj)

        if not size_db:
            logger.error(f"Size with id '{size_id}' not found in the system.")
            raise SizeNotFound(
                size_id=size_id,
                message=ErrorMessage.SIZE_NOT_FOUND.format(size_id=size_id),
            )
        await size_dao.delete_size(db_obj, size_db)
        return {"status": f"Size deleted successfully"}

    async def get_all_size(self, json: Jsonbody, db_obj: AsyncSession):
        """
        Service function to fetch user role asynchronously.
        :param: db_obj: The Async session object
        :param: payload: The search payload
        """
        response = await size_dao.all_size(
            db_obj=db_obj,
            search=json.search,
            sort_by=json.sort_by,
            sort_order=json.sort_order,
            limit=json.limit,
            offset=json.offset,
        )
        return Converter.size_response_db_to_dto(response)

    async def get_all_distinct_size(
        self,
        json: Jsonbody,
        db_obj: AsyncSession,
        category_id: Optional[UUID] = None,
        subcategory_id: Optional[List[UUID]] = None,
    ):
        response = await size_dao.all_filtered_size(
            db_obj=db_obj,
            search=json.search,
            sort_by=json.sort_by,
            sort_order=json.sort_order,
            limit=json.limit,
            offset=json.offset,
            category_id=category_id,
            subcategory_id=subcategory_id,
        )
        return Converter.size_response_db_to_dto(response)


size_service = SizeService()
