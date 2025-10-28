from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.service.subproduct_converter import Converter
from src.dto.subproduct import (
    SubproductCreate,
    SubproductUpdate,
    SubproductUpdateStatus,
)
from src.dao.db import transaction
from src.dao.subproduct import subproduct_dao
from src.exceptions.user import UnauthorizedUser
from src.exceptions.subproduct import SubproductNotFound
from src.utils.user_id import ADMIN_USER_ID
from src.dto.common import SubproductSearchPayload
from src.utils.constants import UuidPrefix
from src.utils.utils import attach_prefix_to_uuid
from typing import List
from src.utils.constants import ErrorMessage
from src.middleware.logger import logger


class SubproductService:
    async def get_single_subproduct_detail(
        self, subproduct_id: UUID, db_obj: AsyncSession
    ):
        """
        Service function to fetch a single subproduct asynchronously and convert it to DTO.
        """
        subproduct_db = await subproduct_dao.fetch_single_subproduct_detail(
            subproduct_id=subproduct_id, db_obj=db_obj
        )

        return Converter.subproduct_detail_db_to_dto(subproduct_db)

    @transaction
    async def create_bulk_subproduct(
        self,
        subproducts_create: List[SubproductCreate],
        user_id: UUID,
        db_obj: AsyncSession,
    ):
        """
        Service function to create a new subproduct asynchronously.
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

        subproduct_ids = [sub.id for sub in subproducts_create]

        existing_subproducts = await subproduct_dao.get_subproducts_by_ids(
            subproduct_ids=subproduct_ids, db_obj=db_obj
        )

        existing_ids = {sp.id for sp in existing_subproducts}

        created_subproducts = []
        existing_subproduct_ids = []
        created_subproducts_ids = []

        for subproduct in subproducts_create:
            if subproduct.id not in existing_ids:
                subproduct_db = Converter.subproduct_create_dto_to_db(subproduct)
                subproduct_db.created_by = admin_user
                subproduct_db.updated_by = admin_user
                created_subproducts.append(subproduct_db)
                created_subproducts_ids.append(str(subproduct.id))
            else:
                existing_subproduct_ids.append(str(subproduct.id))

        subproducts = await subproduct_dao.create_bulk_subproduct(
            db_obj=db_obj, subproducts=created_subproducts
        )

        return {
            "created_subproduct_count": len(created_subproducts_ids),
            "existing_subproduct_count": len(existing_subproduct_ids),
            "data": [Converter.subproduct_db_to_dto(s) for s in subproducts],
            "created_subproduct_ids": created_subproducts_ids,
            "existing_subproduct_ids": existing_subproduct_ids,
        }

    @transaction
    async def update_existing_subproduct(
        self,
        subproduct_id: UUID,
        subproduct_update: SubproductUpdate,
        user_id: UUID,
        db_obj: AsyncSession,
    ):
        """
        Service function to update an existing subproduct asynchronously.
        :param db_obj: The session object
        :param subproduct_id: The ID of the subproduct to update
        :param subproduct_update: The subproduct update DTO
        :param user_id: The ID of the user performing the update
        :return: Updated subproduct object (DTO) or None
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

        subproduct_db = await subproduct_dao.get_subproduct_by_id(
            subproduct_id=subproduct_id, db_obj=db_obj
        )

        subproduct_db.updated_by = admin_user
        if not subproduct_db:
            logger.error(
                f"Subproduct with id '{subproduct_id}' not found in the system."
            )
            raise SubproductNotFound(
                subproduct_id=subproduct_id,
                message=ErrorMessage.SUBPRODUCT_NOT_FOUND.format(
                    subproduct_id=subproduct_id
                ),
            )

        update_subproduct = Converter.subproduct_update_dto_to_db(
            subproduct_update, subproduct_db
        )
        updated_subproduct = await subproduct_dao.update_subproduct(
            db_obj, update_subproduct, subproduct_update
        )
        return Converter.subproduct_db_to_dto(updated_subproduct)

    @transaction
    async def delete_existing_subproduct(
        self, subproduct_id: UUID, user_id: UUID, db_obj: AsyncSession
    ):
        """
        Service function to delete a subproduct asynchronously.
        :param db_obj: The session object
        :param subproduct_id: The ID of the subproduct to delete
        :param user_id: The ID of the user performing the subproduct deletion
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

        subproduct_db = await subproduct_dao.get_subproduct_by_id(
            subproduct_id=subproduct_id, db_obj=db_obj
        )

        if not subproduct_db:
            logger.error(
                f"Subproduct with id '{subproduct_id}' not found in the system."
            )
            raise SubproductNotFound(
                subproduct_id=subproduct_id,
                message=ErrorMessage.SUBPRODUCT_NOT_FOUND.format(
                    subproduct_id=subproduct_id
                ),
            )

        await subproduct_dao.delete_subproduct(db_obj, subproduct_db)
        return {"status": f"Subproduct deleted successfully"}

    async def get_all_subproduct_with_product_detail(
        self, payload: SubproductSearchPayload, db_obj: AsyncSession
    ):
        """
        Service function to fetch subproducts asynchronously.
        """
        response = await subproduct_dao.all_subproduct_fetching_detail(
            db_obj=db_obj,
            search=payload.search,
            sort_by=payload.sort_by,
            sort_order=payload.sort_order,
            limit=payload.limit,
            offset=payload.offset,
            min_rating=getattr(payload.filter, "min_rating", None),
            max_rating=getattr(payload.filter, "max_rating", None),
            min_price=getattr(payload.filter, "min_price", None),
            max_price=getattr(payload.filter, "max_price", None),
            color=getattr(payload.filter, "color", None),
            size=getattr(payload.filter, "size", None),
            category=getattr(payload.filter, "category", None),
            subcategory=getattr(payload.filter, "subcategory", None),
            status=getattr(payload.filter, "status", None),
        )
        return Converter.subproduct_detail_response_db_to_dto(response)

    @transaction
    async def change_subproduct_status(
        self,
        db_obj: AsyncSession,
        subproduct_id: UUID,
        user_id: UUID,
        subproduct_update_status: SubproductUpdateStatus,
    ):
        """
        Service function to change the status of a subproduct asynchronously.
        :param db_obj: The session object
        :param subproduct_id: The ID of the subproduct to update
        :param subproduct_update_status: The status update schema from subproduct dto
        :return: Updated status of the subproduct
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

        subproduct_db = await subproduct_dao.get_subproduct_by_id(subproduct_id, db_obj)
        subproduct_db.updated_by = admin_user
        if not subproduct_db:
            logger.error(
                f"Subproduct with id '{subproduct_id}' not found in the system."
            )
            raise SubproductNotFound(
                subproduct_id=subproduct_id,
                message=ErrorMessage.SUBPRODUCT_NOT_FOUND.format(
                    subproduct_id=subproduct_id
                ),
            )

        updated_subproduct = await subproduct_dao.update_subproduct_status(
            db_obj, subproduct_db, subproduct_update_status.status
        )
        return Converter.subproduct_db_to_dto(updated_subproduct)


subproduct_service = SubproductService()
