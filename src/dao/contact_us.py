from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.dao.models.user import ContactUs
from src.dto.contact_us import ContactUsCreate, ContactUsUpdate
from uuid import UUID
from typing import Optional
from sqlalchemy import or_
from src.dao.models.user import ContactUs


class contact_us_dao:
    async def get_contact_us(contact_us_id: UUID, db_obj: AsyncSession):
        """
        This function gets a contact us details from the database by using their contact us id.
        :param contact_us_id: Id of the contact us.
        :param db_obj: AsyncSession: Pass the database asynchronous session object to the function
        """
        result = await db_obj.execute(
            select(ContactUs).where(ContactUs.id == contact_us_id)
        )
        return result.scalars().first()

    async def create_contact_us(db_obj: AsyncSession, contact_us: ContactUsCreate):
        """
        This function creates a contact us details in the database.

        :param contact_us: contact us creation request payload schema.
        :param db_obj: database object
        """
        db_obj.add(contact_us)
        await db_obj.commit()
        await db_obj.refresh(contact_us)
        return contact_us

    async def update_contact_us(
        db_obj: AsyncSession, contact_us_db: ContactUs, contact_us: ContactUsUpdate
    ):
        """
        This function update a contact us details in the database.

        :param contact_us: contact us(dto) to update request payload schema.
        :param contact_us_db: Database of the contact us to be updated.
        :param db_obj: database object
        """
        for key, value in contact_us.dict(exclude_unset=True).items():
            setattr(contact_us_db, key, value)
        return contact_us_db

    async def delete_contact_us(db_obj: AsyncSession, contact_us: ContactUs):
        """
        This function deletes the contact us details from the database.
        :param contact_us: Database of the contact us to be updated.
        :param db_obj: database object
        """
        await db_obj.delete(contact_us)

    async def all_contact_us_details(
        db_obj: AsyncSession,
        search: Optional[str] = None,
        sort_by: Optional[str] = "created_at",
        sort_order: Optional[str] = "asc",
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
    ):
        """
        The all_contact_us_details function is used to retrieve all the contact us details in the database.
        It takes in a number of parameters that are used to filter and sort the results.
        :param search: Used to searching
        :param sort_order: Determine if the query should be sorted in ascending or descending order
        :param sort_by: Sort the results by a particular column
        :param limit: Limit the number of results returned
        :param offset: Skip the first n records
        :param db_obj: database object

        :return: all contact us by applying filter and sorting
        """
        filters = []

        if search:
            filters.append(or_(ContactUs.message.ilike(f"%{search}%")))

        query = select(ContactUs)
        if filters:
            query = query.where(*filters)

        if sort_by:
            if sort_order == "asc":
                query = query.order_by(getattr(ContactUs, sort_by).asc())
            elif sort_order == "desc":
                query = query.order_by(getattr(ContactUs, sort_by).desc())

        query = query.limit(limit).offset(offset)
        result = await db_obj.execute(query)
        return result.scalars().all()
