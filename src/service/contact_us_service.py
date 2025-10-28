from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.service.user_converter import Converter
from src.dao.db import transaction
from src.dto.contact_us import ContactUsCreate, ContactUsUpdate
from src.dao.contact_us import contact_us_dao
from src.exceptions.contact_us import ContactUsNotFound
from src.dto.common import Jsonbody
from src.utils.constants import ErrorMessage
from src.middleware.logger import logger


class ContactUsService:
    @transaction
    async def get_contact_us_by_id(self, contact_us_id: UUID, db_obj: AsyncSession):
        """
        Service function to get a contact us by ID asynchronously.
        :param db: The session object
        :param contact_us_id: The ID of the contact us to retrieve
        :return: contact us object or None
        """
        result = await contact_us_dao.get_contact_us(
            contact_us_id=contact_us_id, db_obj=db_obj
        )
        if not result:
            logger.error(
                f"Contact us details with id '{contact_us_id}' not found in the system."
            )
            raise ContactUsNotFound(
                contact_us_id=contact_us_id,
                message=ErrorMessage.CONTACT_US_NOT_FOUND.format(
                    contact_us_id=contact_us_id
                ),
            )
        return result

    @transaction
    async def create_contact_us_details(
        self, contact_us_create: ContactUsCreate, db_obj: AsyncSession
    ):
        """
        Service function to create a new contact us asynchronously.
        :param db: The session object
        :param contact_us_create: The contact us creation DTO
        :return: Created contact us object (DTO)
        """
        contact_us_db = Converter.contact_us_create_dto_to_db(contact_us_create)
        contact_us = await contact_us_dao.create_contact_us(db_obj, contact_us_db)
        return Converter.contact_us_db_to_dto(contact_us)

    @transaction
    async def update_existing_contact_us(
        self,
        contact_us_id: UUID,
        contact_us_update: ContactUsUpdate,
        db_obj: AsyncSession,
    ):
        """
        Service function to update an existing contact us asynchronously.
        :param db: The session object
        :param contact_us_id: The ID of the contact us to update
        :param contact_us_update: The contact us update DTO
        :return: Updated contact us object (DTO) or None
        """
        contact_us_db = await contact_us_dao.get_contact_us(contact_us_id, db_obj)
        if not contact_us_db:
            logger.error(
                f"Contact us details with id '{contact_us_id}' not found in the system."
            )
            raise ContactUsNotFound(
                contact_us_id=contact_us_id,
                message=ErrorMessage.CONTACT_US_NOT_FOUND.format(
                    contact_us_id=contact_us_id
                ),
            )
        update_contact_us = Converter.contact_us_update_dto_to_db(
            contact_us_update, contact_us_db
        )
        updated_contact_us = await contact_us_dao.update_contact_us(
            db_obj, update_contact_us, contact_us_update
        )
        return Converter.contact_us_db_to_dto(updated_contact_us)

    @transaction
    async def delete_existing_contact_us(
        self, contact_us_id: UUID, db_obj: AsyncSession
    ):
        """
        Service function to delete a contact us asynchronously.
        :param db: The session object
        :param contact_us_id: The ID of the contact us to delete
        :return: Dictionary with success status
        """
        contact_us_db = await contact_us_dao.get_contact_us(contact_us_id, db_obj)
        if not contact_us_db:
            logger.error(
                f"Contact us details with id '{contact_us_id}' not found in the system."
            )
            raise ContactUsNotFound(
                contact_us_id=contact_us_id,
                message=ErrorMessage.CONTACT_US_NOT_FOUND.format(
                    contact_us_id=contact_us_id
                ),
            )
        await contact_us_dao.delete_contact_us(db_obj, contact_us_db)
        return {"status": "Success"}

    async def get_all_contact_us(self, db_obj: AsyncSession, json: Jsonbody):
        """
        Service function to fetch contact us asynchronously.
        :param: db_obj: The Async session object
        :param: payload: The search payload
        """
        contact_us = await contact_us_dao.all_contact_us_details(
            db_obj=db_obj,
            search=json.search,
            sort_by=json.sort_by,
            sort_order=json.sort_order,
            limit=json.limit,
            offset=json.offset,
        )
        return [Converter.contact_us_db_to_dto(contacts) for contacts in contact_us]


contact_us_service = ContactUsService()
