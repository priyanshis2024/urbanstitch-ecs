from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.service.user_converter import Converter
from src.dao.db import transaction
from src.dto.common import Jsonbody
from src.dto.customer_details import CustomerDetailCreate, CustomerDetailUpdate
from src.exceptions.user import UnauthorizedUser
from src.exceptions.customer_detail import CustomerDetailNotFound
from src.dao.customer_details import customer_detail_dao
from src.utils.user_id import ADMIN_USER_ID
from src.utils.constants import ErrorMessage
from src.middleware.logger import logger


class CustomerDetailService:
    @transaction
    async def get_customer_detail_by_id(
        self, customer_detail_id: UUID, db_obj: AsyncSession
    ):
        """
        Service function to get a customer_detail by ID asynchronously.
        :param db: The session object
        :param customer_detail_id: The ID of the customer_detail to retrieve
        :return: customer_detail object or None
        """
        result = await customer_detail_dao.get_customer_detail(
            customer_detail_id=customer_detail_id, db_obj=db_obj
        )
        if not result:
            logger.error(
                f"Customer with id '{customer_detail_id}' not found in the system."
            )
            raise CustomerDetailNotFound(
                customer_detail_id=str(customer_detail_id),
                message=ErrorMessage.CUSTOMER_DETAIL_NOT_FOUND.format(
                    customer_detail_id=customer_detail_id
                ),
            )
        return result

    @transaction
    async def create_customer_detail_details(
        self,
        customer_detail_create: CustomerDetailCreate,
        user_id: UUID,
        db_obj: AsyncSession,
    ):
        """
        Service function to create a new customer_detail asynchronously.
        :param db: The session object
        :param customer_detail_create: The customer_detail creation DTO
        :return: Created customer_detail object (DTO)
        """
        if user_id == ADMIN_USER_ID:
            logger.error(
                f"Unauthorized user. User with id '{user_id}' is not authorized user to access this resource."
            )
            raise UnauthorizedUser(
                user_id=user_id,
                message=ErrorMessage.UNAUTHORIZED_USER.format(user_id=user_id),
            )
        customer_detail_db = Converter.customer_detail_create_dto_to_db(
            customer_detail_create
        )
        customer_detail_db.user_id = user_id
        customer_detail = await customer_detail_dao.create_customer_detail(
            db_obj, customer_detail_db
        )
        return Converter.customer_detail_db_to_dto(customer_detail)

    @transaction
    async def update_existing_customer_detail(
        self,
        customer_detail_id: UUID,
        customer_detail_update: CustomerDetailUpdate,
        user_id: UUID,
        db_obj: AsyncSession,
    ):
        """
        Service function to update an existing customer_detail asynchronously.
        :param db: The session object
        :param customer_detail_id: The ID of the customer_detail to update
        :param customer_detail_update: The customer_detail update DTO
        :return: Updated customer_detail object (DTO) or None
        """
        if user_id == ADMIN_USER_ID:
            logger.error(
                f"Unauthorized user. User with id '{user_id}' is not authorized user to access this resource."
            )
            raise UnauthorizedUser(
                user_id=user_id,
                message=ErrorMessage.UNAUTHORIZED_USER.format(user_id=user_id),
            )
        customer_detail_db = await customer_detail_dao.get_customer_detail(
            customer_detail_id, db_obj
        )
        if not customer_detail_db:
            logger.error(
                f"Customer with id '{customer_detail_id}' not found in the system."
            )
            raise CustomerDetailNotFound(
                customer_detail_id=str(customer_detail_id),
                message=ErrorMessage.CUSTOMER_DETAIL_NOT_FOUND.format(
                    customer_detail_id=customer_detail_id
                ),
            )
        update_customer_detail = Converter.customer_detail_update_dto_to_db(
            customer_detail_update, customer_detail_db
        )
        update_customer_detail.user_id = user_id
        updated_customer_detail = await customer_detail_dao.update_customer_detail(
            db_obj, update_customer_detail, customer_detail_update
        )
        return Converter.customer_detail_db_to_dto(updated_customer_detail)

    @transaction
    async def delete_existing_customer_detail(
        self, customer_detail_id: UUID, user_id: UUID, db_obj: AsyncSession
    ):
        """
        Service function to delete a customer_detail asynchronously.
        :param db: The session object
        :param customer_detail_id: The ID of the customer_detail to delete
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
        customer_detail_db = await customer_detail_dao.get_customer_detail(
            customer_detail_id, db_obj
        )
        if not customer_detail_db:
            logger.error(
                f"Customer with id '{customer_detail_id}' not found in the system."
            )
            raise CustomerDetailNotFound(
                customer_detail_id=str(customer_detail_id),
                message=ErrorMessage.CUSTOMER_DETAIL_NOT_FOUND.format(
                    customer_detail_id=customer_detail_id
                ),
            )
        customer_detail_db.user_id = user_id
        await customer_detail_dao.delete_customer_detail(db_obj, customer_detail_db)
        return {"status": "Success"}

    async def get_all_customer_detail(self, json: Jsonbody, db_obj: AsyncSession):
        """
        Service function to fetch customer_detail asynchronously.
        :param: db_obj: The Async session object
        :param: json: The search json data
        """
        customer_detailes = await customer_detail_dao.all_customer_detail(
            db_obj=db_obj,
            search=json.search,
            sort_by=json.sort_by,
            sort_order=json.sort_order,
            limit=json.limit,
            offset=json.offset,
        )
        return [
            Converter.customer_detail_db_to_dto(customer_detail)
            for customer_detail in customer_detailes
        ]

    async def get_customers_details_by_user_id(
        self, user_id: UUID, db_obj: AsyncSession
    ):
        """
        Service function to fetch customers_details by user_id asynchronously.
        :param: db_obj: The Async session object
        :param: user_id: The user id
        """
        customer_detail = await customer_detail_dao.get_customers_details_by_user_id(
            db_obj=db_obj, user_id=user_id
        )
        return Converter.customers_details_summary_db_to_dto(customer_detail)


customer_detail_service = CustomerDetailService()
