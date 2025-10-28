from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.service.category_converter import Converter
from src.service.subcategory_converter import Converter as subcategory_converter
from src.service.category_xref_converter import Converter as category_xref_converter
from src.dto.category import (
    CategoryCreate,
    CategoryUpdate,
    DeleteCategoryResponse,
    DeleteCategoryRequest,
    CategoryUpdateStatus,
)
from src.dto.subcategory import SubcategoryDeleteRequest
from src.dto.category_xref import CategoryXrefCreate
from src.dao.db import transaction
from src.dao.category import category_dao
from src.dao.subcategory import subcategory_dao
from src.dao.category_xref import category_xref_dao
from src.exceptions.user import UnauthorizedUser
from src.exceptions.category import CategoryNotFound, CategoryAlreadyExists
from src.utils.user_id import ADMIN_USER_ID
from typing import Optional, List
from src.dto.common import Jsonbody
from src.utils.constants import UuidPrefix
from src.utils.utils import attach_prefix_to_uuid
from src.utils.constants import ErrorMessage
from src.middleware.logger import logger


class CategoryService:
    async def get_category_by_id(self, category_id: UUID, db_obj: AsyncSession):
        result = await category_dao.get_category_by_id(
            category_id=category_id, db_obj=db_obj
        )
        if not result:
            logger.error(f"Category with id '{category_id}' not found in the system.")
            raise CategoryNotFound(
                category_id=category_id,
                message=ErrorMessage.CATEGORY_NOT_FOUND.format(category_id=category_id),
            )
        return result

    async def get_category_by_id_with_subcategory(
        self, category_id: UUID, db_obj: AsyncSession
    ):
        category_data = await category_dao.get_category(
            category_id=category_id, db_obj=db_obj
        )

        if not category_data:
            logger.error(f"Category with id '{category_id}' not found in the system.")
            raise CategoryNotFound(
                category_id=category_id,
                message=ErrorMessage.CATEGORY_NOT_FOUND.format(category_id=category_id),
            )

        category, subcategories = category_data

        return Converter.category_db_to_dto(category, subcategories)

    @transaction
    async def create_category(
        self, category_create: CategoryCreate, user_id: UUID, db_obj: AsyncSession
    ):
        """
        Service function to create a new category along with their subcategory asynchronously.
        :param db: The session object
        :param category_create: The category creation DTO
        :return: Created category object (DTO)
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

        existing_category = await category_dao.get_category_by_id(
            category_create.id, db_obj
        )
        if existing_category:
            logger.error(
                f"Category with id '{category_create.id}' already exists in the system."
            )
            raise CategoryAlreadyExists(
                category_id=category_create.id,
                message=ErrorMessage.CATEGORY_ALREADY_EXISTS.format(
                    category_id=category_create.id
                ),
            )

        category_db = Converter.category_create_dto_to_db(category_create)
        category_db.created_by = admin_user
        category_db.updated_by = admin_user

        await category_dao.create_category(category_db, db_obj)

        for subcategory_data in category_create.subcategories:

            existing_subcategory = await subcategory_dao.get_subcategory_by_id(
                subcategory_data.id, db_obj
            )

            if not existing_subcategory:
                subcategory = subcategory_converter.subcategory_create_dto_to_db(
                    subcategory_data
                )
                subcategory.created_by = admin_user
                subcategory.updated_by = admin_user
                await subcategory_dao.create_subcategory(subcategory, db_obj)
            else:
                subcategory = existing_subcategory

            existing_xref = await category_xref_dao.get_category_xref(
                db_obj, category_db.id, subcategory.id
            )

            if not existing_xref:
                category_xref_create = CategoryXrefCreate(
                    category_id=category_db.id,
                    subcategory_id=subcategory.id,
                    subcategories_type=subcategory_data.subcategories_type,
                )
                category_xref = category_xref_converter.category_xref_create_dto_to_db(
                    category_xref_create
                )
                await category_xref_dao.create_category_xref(category_xref, db_obj)

        subcategories = await category_xref_dao.get_subcategories_by_category_id(
            db_obj, category_db.id
        )
        return Converter.category_db_to_dto(category_db, subcategories)

    @transaction
    async def create_bulk_categories(
        self,
        categories_create: List[CategoryCreate],
        user_id: UUID,
        db_obj: AsyncSession,
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

        category_ids = [cat.id for cat in categories_create]
        subcategory_ids = [
            sub.id for cat in categories_create for sub in cat.subcategories
        ]

        existing_categories = await category_dao.get_categories_by_ids(
            db_obj, category_ids
        )
        existing_subcategories = await subcategory_dao.get_subcategories_by_ids(
            db_obj, subcategory_ids
        )

        created_categories = []
        created_categories_ids = []
        existing_categories_ids = []
        created_subcategories_ids = []
        existing_subcategories_ids = []

        for category_create in categories_create:
            if category_create.id in existing_categories:
                existing_categories_ids.append(category_create.id)
                continue

            category_db = Converter.category_create_dto_to_db(category_create)
            category_db.created_by = admin_user
            category_db.updated_by = admin_user
            await category_dao.create_category(category_db, db_obj)
            created_categories_ids.append(category_db.id)

            for subcategory_data in category_create.subcategories:
                subcategory_id = subcategory_data.id

                if subcategory_id not in existing_subcategories:
                    subcategory = subcategory_converter.subcategory_create_dto_to_db(
                        subcategory_data
                    )
                    subcategory.created_by = admin_user
                    subcategory.updated_by = admin_user
                    await subcategory_dao.create_subcategory(subcategory, db_obj)
                    created_subcategories_ids.append(subcategory.id)
                else:
                    subcategory = existing_subcategories[subcategory_id]
                    existing_subcategories_ids.append(subcategory.id)

                existing_xref = await category_xref_dao.get_category_xref(
                    db_obj, category_db.id, subcategory.id
                )

                if not existing_xref:
                    category_xref_create = CategoryXrefCreate(
                        category_id=category_db.id,
                        subcategory_id=subcategory.id,
                        subcategories_type=subcategory_data.subcategories_type,
                    )
                    category_xref = (
                        category_xref_converter.category_xref_create_dto_to_db(
                            category_xref_create
                        )
                    )
                    await category_xref_dao.create_category_xref(category_xref, db_obj)

            subcategories = await category_xref_dao.get_subcategories_by_category_id(
                db_obj, category_db.id
            )
            created_categories.append(
                Converter.category_db_to_dto(category_db, subcategories)
            )

        return {
            "created_categories_count": len(created_categories_ids),
            "existing_categories_count": len(existing_categories_ids),
            "created_subcategories_count": len(created_subcategories_ids),
            "existing_subcategories_count": len(existing_subcategories_ids),
            "data": created_categories,
            "created_categories_ids": created_categories_ids,
            "existing_categories_ids": existing_categories_ids,
            "created_subcategories_ids": created_subcategories_ids,
            "existing_subcategories_ids": existing_subcategories_ids,
        }

    @transaction
    async def update_category(
        self,
        category_id: UUID,
        category_update: CategoryUpdate,
        user_id: UUID,
        db_obj: AsyncSession,
    ):
        """
        Updates a category and its associated subcategories.
        Uses DAO for DB interactions and Converter for DTO transformations.
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

        category_db = await category_dao.get_category_by_id(category_id, db_obj)
        if not category_db:
            logger.error(f"Category with id '{category_id}' not found in the system.")
            raise CategoryNotFound(
                category_id=category_id,
                message=ErrorMessage.CATEGORY_NOT_FOUND.format(category_id=category_id),
            )

        update_category = Converter.category_update_dto_to_db(
            category_update, category_db
        )
        update_category.updated_by = admin_user

        await category_dao.update_category(db_obj, update_category, category_update)

        for subcategory_data in category_update.subcategories:
            existing_subcategory = await subcategory_dao.get_subcategory_by_id(
                subcategory_data.id, db_obj
            )

            if existing_subcategory:
                subcategory_update_data = (
                    subcategory_converter.subcategory_update_dto_to_db(
                        subcategory_data, existing_subcategory
                    )
                )
                subcategory_update_data.updated_by = admin_user
                await subcategory_dao.update_subcategory(
                    db_obj, subcategory_update_data, subcategory_data
                )
                subcategory_id = existing_subcategory.id
            else:
                new_subcategory = subcategory_converter.subcategory_create_dto_to_db(
                    subcategory_data
                )
                new_subcategory.created_by = admin_user
                new_subcategory.updated_by = admin_user
                await subcategory_dao.create_subcategory(new_subcategory, db_obj)
                subcategory_id = new_subcategory.id

            existing_xref = await category_xref_dao.get_category_xref(
                db_obj, category_id, subcategory_id
            )

            if not existing_xref:
                category_xref_create = CategoryXrefCreate(
                    category_db.id, subcategory_id
                )
                category_xref = category_xref_converter.category_xref_create_dto_to_db(
                    category_xref_create
                )
                await category_xref_dao.create_category_xref(category_xref, db_obj)

        subcategories = await category_xref_dao.get_subcategories_by_category_id(
            db_obj, category_db.id
        )
        return Converter.category_db_to_dto(category_db, subcategories)

    @transaction
    async def delete_category(
        self,
        category_id: UUID,
        user_id: UUID,
        db_obj: AsyncSession,
        request_body: Optional[DeleteCategoryRequest] = None,
    ) -> DeleteCategoryResponse:
        if user_id != ADMIN_USER_ID:
            logger.error(
                f"Unauthorized user. User with id '{user_id}' is not authorized user to access this resource."
            )
            raise UnauthorizedUser(
                user_id=user_id,
                message=ErrorMessage.UNAUTHORIZED_USER.format(user_id=user_id),
            )
        category_db = await category_dao.get_category_by_id(
            category_id=category_id, db_obj=db_obj
        )
        if not category_db:
            logger.error(f"Category with id '{category_id}' not found in the system.")
            raise CategoryNotFound(
                category_id=category_id,
                message=ErrorMessage.CATEGORY_NOT_FOUND.format(category_id=category_id),
            )
        deleted_subcategories = []
        remaining_subcategories = []

        if request_body and request_body.subcategories:
            for subcategory_data in request_body.subcategories:
                subcategory = await subcategory_dao.get_subcategory_by_id(
                    subcategory_id=subcategory_data.id, db_obj=db_obj
                )
                if not subcategory:
                    continue

                existing_mapping = await category_xref_dao.get_category_xref(
                    db_obj, category_id, subcategory_data.id
                )
                if existing_mapping:
                    await category_xref_dao.delete_category_xrefs_category_id_or_subcategory_id(
                        db_obj, category_id, subcategory_id=subcategory_data.id
                    )

                remaining_mappings = await category_xref_dao.get_category_xref(
                    db_obj, subcategory_data.id
                )

                if not remaining_mappings:
                    await subcategory_dao.delete_subcategory(subcategory, db_obj)
                    deleted_subcategories.append(
                        SubcategoryDeleteRequest(
                            id=subcategory.id, name=subcategory.name
                        )
                    )

            subcategories = await category_xref_dao.get_subcategories_by_category_id(
                db_obj, category_id
            )
            remaining_subcategories = [
                SubcategoryDeleteRequest(id=sub.id, name=sub.name)
                for sub in subcategories
            ]

            status_message = (
                f"Deleted specified subcategories from category '{category_db.name}'."
            )

        else:
            subcategory_ids = (
                await category_xref_dao.get_subcategory_ids_by_category_id(
                    db_obj, category_id
                )
            )

            if subcategory_ids:
                await category_xref_dao.delete_category_xrefs_category_id_or_subcategory_id(
                    db_obj, category_id
                )
                for subcategory_id in subcategory_ids:
                    remaining_mappings = await category_xref_dao.get_category_xref(
                        db_obj=db_obj, subcategory_id=subcategory_id
                    )

                    if not remaining_mappings:
                        subcategory = await subcategory_dao.get_subcategory_by_id(
                            subcategory_id=subcategory_id, db_obj=db_obj
                        )
                        if subcategory:
                            await subcategory_dao.delete_subcategory(
                                subcategory, db_obj
                            )
                            deleted_subcategories.append(
                                SubcategoryDeleteRequest(
                                    id=subcategory.id, name=subcategory.name
                                )
                            )

            await category_dao.delete_category(category_db, db_obj)
            status_message = f"Category '{category_db.name}' deleted successfully."

        return DeleteCategoryResponse(
            status=status_message,
            category_id=category_db.id,
            category_name=category_db.name,
            deleted_subcategories=deleted_subcategories or None,
            remaining_subcategories=remaining_subcategories or None,
        )

    async def get_all_category(self, json: Jsonbody, db_obj: AsyncSession):
        """
        Service function to fetch subproducts asynchronously.
        """
        response = await category_dao.all_category(
            db_obj=db_obj,
            search=json.search,
            sort_by=json.sort_by,
            sort_order=json.sort_order,
            limit=json.limit,
            offset=json.offset,
        )
        return Converter.category_response_db_to_dto(response)

    @transaction
    async def change_category_status(
        self,
        db_obj: AsyncSession,
        category_id: UUID,
        user_id: UUID,
        category_update_status: CategoryUpdateStatus,
    ):
        """
        Service function to change the status of a category asynchronously.
        :param db_obj: The session object
        :param category_id: The ID of the category to update
        :param category_update_status: The status update schema from category dto
        :return: Updated status of the category
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

        category_db = await category_dao.get_category_by_id(category_id, db_obj)
        if not category_db:
            logger.error(f"Category with id '{category_id}' not found in the system.")
            raise CategoryNotFound(
                category_id=category_id,
                message=ErrorMessage.CATEGORY_NOT_FOUND.format(category_id=category_id),
            )
        category_db.updated_by = admin_user
        updated_category = await category_dao.update_category_status(
            db_obj, category_db, category_update_status.status
        )
        return Converter.category_db_to_dto(updated_category)


category_service = CategoryService()
