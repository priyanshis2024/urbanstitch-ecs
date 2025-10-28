from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.dao.models.product import Subproduct
from src.service.product_converter import Converter
from src.dto.product import ProductCreate, ProductUpdate, ProductUpdateStatus
from src.dao.db import transaction
from src.dao.products import product_dao
from src.dao.subproduct import subproduct_dao
from src.service.product_converter import Converter
from src.exceptions.user import UnauthorizedUser
from src.exceptions.product import ProductNotFound
from src.utils.user_id import ADMIN_USER_ID
from src.dto.common import ProductSearchPayload
from src.utils.constants import UuidPrefix
from src.utils.utils import attach_prefix_to_uuid
from typing import List
from src.utils.constants import ErrorMessage
from src.middleware.logger import logger


class ProductService:
    async def get_product_by_id(self, product_id: UUID, db_obj: AsyncSession):
        """
        Service function to get a product by ID asynchronously.
        :param db_obj: The session object
        :param product_id: The ID of the product to retrieve
        :return: product object or None
        """
        result = await product_dao.get_product_by_id(product_id, db_obj=db_obj)
        if not result:
            logger.error(f"Product with id '{product_id}' not found in the system.")
            raise ProductNotFound(
                product_id=product_id,
                message=ErrorMessage.PRODUCT_NOT_FOUND.format(product_id=product_id),
            )
        product_db = await product_dao.get_product_by_id(product_id, db_obj=db_obj)
        return Converter.product_description_db_to_dto(product_db)

    @transaction
    async def create_product_details(
        self, product_create: ProductCreate, user_id: UUID, db_obj: AsyncSession
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

        product_db = Converter.product_create_dto_to_db(product_create)
        product_db.created_by = admin_user
        product_db.updated_by = admin_user

        await product_dao.create_product(db_obj, product_db)

        for subproduct_data in product_create.subproducts:
            existing_subproduct = await subproduct_dao.get_subproduct_by_id(
                subproduct_data.id, db_obj
            )
            if not existing_subproduct:
                subproduct = Subproduct(
                    id=subproduct_data.id,
                    product_id=product_db.id,
                    size_id=subproduct_data.size_id,
                    price=subproduct_data.price,
                    color=subproduct_data.color,
                    quantity=subproduct_data.quantity,
                    images=subproduct_data.images,
                    created_by=admin_user,
                    updated_by=admin_user,
                )
                await subproduct_dao.create_subproduct(db_obj, subproduct)
            else:
                subproduct = existing_subproduct

        await product_dao.create_product(db_obj, product_db)
        return Converter.product_db_to_dto(product_db)

    @transaction
    async def create_bulk_product_details(
        self, products_create: List[ProductCreate], user_id: UUID, db_obj: AsyncSession
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

        product_ids = [p.id for p in products_create]
        subproduct_ids = [s.id for p in products_create for s in p.subproducts]

        existing_products = await product_dao.get_products_by_ids(db_obj, product_ids)
        existing_subproducts = await subproduct_dao.get_subproducts_by_ids(
            db_obj, subproduct_ids
        )

        created_products = []
        created_products_ids = []
        existing_products_ids = []
        created_subproducts_ids = []
        existing_subproducts_ids = []

        for product_create in products_create:
            if product_create.id in existing_products:
                existing_products_ids.append(product_create.id)
                continue

            product_db = Converter.product_create_dto_to_db(product_create)
            product_db.created_by = admin_user
            product_db.updated_by = admin_user
            await product_dao.create_product(db_obj, product_db)
            created_products_ids.append(product_create.id)
            created_products.append(Converter.product_db_to_dto(product_db))

            for subproduct_data in product_create.subproducts:
                subproduct_id = subproduct_data.id

                if subproduct_id not in existing_subproducts:
                    subproduct = Subproduct(
                        id=subproduct_data.id,
                        product_id=product_db.id,
                        size_id=subproduct_data.size_id,
                        price=subproduct_data.price,
                        color=subproduct_data.color,
                        quantity=subproduct_data.quantity,
                        images=subproduct_data.images,
                        created_by=admin_user,
                        updated_by=admin_user,
                    )
                    await subproduct_dao.create_subproduct(db_obj, subproduct)
                    created_subproducts_ids.append(subproduct.id)
                else:
                    subproduct = existing_subproducts[subproduct_id]
                    existing_subproducts_ids.append(subproduct_id)

        subproducts = await subproduct_dao.get_subproducts_by_ids(
            db_obj, subproduct_ids
        )

        return {
            "created_product_count": len(created_products_ids),
            "existing_product_count": len(existing_products_ids),
            "created_subproduct_count": len(created_subproducts_ids),
            "existing_subproduct_count": len(existing_subproducts_ids),
            "data": created_products,
            "created_products_ids": created_products_ids,
            "existing_products_ids": existing_products_ids,
            "created_subproducts_ids": created_subproducts_ids,
            "existing_subproducts_ids": existing_subproducts_ids,
        }

    @transaction
    async def update_product_rating(self, product_id: UUID, db_obj: AsyncSession):
        """
        Recalculate and update the product rating based on all reviews.
        """
        average_rating = await product_dao.calculate_average_product_rating(
            db_obj, product_id
        )
        new_rating = round(average_rating, 1) if average_rating else 0.0

        product = await product_dao.get_product_by_id(
            product_id=product_id, db_obj=db_obj
        )
        if product:
            product.rating = new_rating

    @transaction
    async def update_existing_product(
        self,
        product_id: UUID,
        product_update: ProductUpdate,
        user_id: UUID,
        db_obj: AsyncSession,
    ):
        """
        Service function to update an existing product asynchronously.
        :param db_obj: The session object
        :param product_id: The ID of the product to update
        :param product_update: The product update DTO
        :param user_id: The ID of the user performing the update
        :return: Updated product object (DTO) or None
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

        product_db = await product_dao.get_product_by_id(
            product_id=product_id, db_obj=db_obj
        )

        product_db.updated_by = admin_user

        if not product_db:
            logger.error(f"Product with id '{product_id}' not found in the system.")
            raise ProductNotFound(
                product_id=product_id,
                message=ErrorMessage.PRODUCT_NOT_FOUND.format(product_id=product_id),
            )

        update_product = Converter.product_update_dto_to_db(product_update, product_db)
        updated_product = await product_dao.update_product(
            db_obj, update_product, product_update
        )
        return Converter.product_detail_db_to_dto(updated_product)

    @transaction
    async def delete_existing_product(
        self,
        product_id: UUID,
        user_id: UUID,
        db_obj: AsyncSession,
    ):
        """
        Service function to delete a product asynchronously.
        """
        if user_id != ADMIN_USER_ID:
            logger.error(
                f"Unauthorized user. User with id '{user_id}' is not authorized user to access this resource."
            )
            raise UnauthorizedUser(
                user_id=user_id,
                message=ErrorMessage.UNAUTHORIZED_USER.format(user_id=user_id),
            )

        product_db = await product_dao.get_product_by_id(product_id, db_obj=db_obj)
        if not product_db:
            logger.error(f"Product with id '{product_id}' not found in the system.")
            raise ProductNotFound(
                product_id=product_id,
                message=ErrorMessage.PRODUCT_NOT_FOUND.format(product_id=product_id),
            )
        await product_dao.delete_product(db_obj, product_db)
        return {
            "status": f"Product {product_id} and all associated subproducts deleted successfully"
        }

    async def get_all_products(
        self, payload: ProductSearchPayload, db_obj: AsyncSession
    ):
        """
        Service function to fetch products asynchronously.
        """
        response = await product_dao.all_products(
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
        return Converter.product_description_list_response_db_to_dto(response)

    @transaction
    async def change_product_status(
        self,
        db_obj: AsyncSession,
        product_id: UUID,
        user_id: UUID,
        product_update_status: ProductUpdateStatus,
    ):
        """
        Service function to change the status of a product asynchronously.
        :param db_obj: The session object
        :param product_id: The ID of the product to update
        :param product_update_status: The status update schema from product dto
        :return: Updated status of the product
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

        product_db = await product_dao.get_product_by_id(product_id, db_obj)
        product_db.updated_by = admin_user
        if not product_db:
            logger.error(f"Product with id '{product_id}' not found in the system.")
            raise ProductNotFound(
                product_id=product_id,
                message=ErrorMessage.PRODUCT_NOT_FOUND.format(product_id=product_id),
            )
        updated_product = await product_dao.update_product_status(
            db_obj, product_db, product_update_status.status
        )
        return Converter.product_db_to_dto(updated_product)


product_service = ProductService()
