from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.dao.models.user import CustomerDetails
from src.dto.customer_details import CustomerDetailCreate, CustomerDetailUpdate
from uuid import UUID
from typing import Optional
from sqlalchemy import or_


class customer_detail_dao:
    async def get_customer_detail(customer_detail_id: UUID, db_obj: AsyncSession):
        """
        This function gets a customer_detail details from the database by using their customer_detail id.
        :param customer_detail_id: Id of the customer detail.
        :param db_obj: AsyncSession: Pass the database asynchronous session object to the function
        """
        result = await db_obj.execute(
            select(CustomerDetails).where(CustomerDetails.id == customer_detail_id)
        )
        return result.scalars().first()

    async def create_customer_detail(
        db_obj: AsyncSession, customer_detail: CustomerDetailCreate
    ):
        """
        This function creates a customer_detail in the database.

        :param customer_detail: customer_detail creation request payload schema.
        :param db_obj: database object
        """
        db_obj.add(customer_detail)
        await db_obj.commit()
        await db_obj.refresh(customer_detail)
        return customer_detail

    async def update_customer_detail(
        db_obj: AsyncSession,
        customer_detail_db: CustomerDetails,
        customer_detail: CustomerDetailUpdate,
    ):
        """
        This function update a customer_detail details in the database.

        :param customer_detail: customer_detail update request payload schema.
        :param customer_detail_db: Database of the customer_detail to be updated.
        :param db_obj: database object
        """
        for key, value in customer_detail.dict(exclude_unset=True).items():
            setattr(customer_detail_db, key, value)
        return customer_detail_db

    async def delete_customer_detail(
        db_obj: AsyncSession, customer_detail: CustomerDetails
    ):
        """
        This function deletes the customer_detail details from the database.
        :param customer_detail: Database of the contact us to be deleted.
        :param db_obj: database object
        """
        await db_obj.delete(customer_detail)

    async def all_customer_detail(
        db_obj: AsyncSession,
        search: Optional[str] = None,
        sort_by: Optional[str] = "created_at",
        sort_order: Optional[str] = "asc",
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
    ):
        """
        The all_customer_detail function is used to retrieve all the customer_details in the database.
        It takes in a number of parameters that are used to filter and sort the results.
        :param search: Used to searching
        :param sort_order: Determine if the query should be sorted in ascending or descending order
        :param sort_by: Sort the results by a particular column
        :param limit: Limit the number of results returned
        :param offset: Skip the first n records
        :param db_obj: database object

        :return: all customer_detail by applying filter and sorting
        """
        filters = []

        if search:
            filters.append(
                or_(
                    CustomerDetails.landmark.ilike(f"%{search}%"),
                    CustomerDetails.address.ilike(f"%{search}%"),
                    CustomerDetails.city.ilike(f"%{search}%"),
                    CustomerDetails.state.ilike(f"%{search}%"),
                    CustomerDetails.country.ilike(f"%{search}%"),
                )
            )

        query = select(CustomerDetails)
        if filters:
            query = query.where(*filters)

        if sort_by and hasattr(CustomerDetails, sort_by):
            order_by_column = getattr(CustomerDetails, sort_by)
            query = query.order_by(
                order_by_column.asc() if sort_order == "asc" else order_by_column.desc()
            )
        query = query.limit(limit).offset(offset)
        result = await db_obj.execute(query)
        return result.scalars().all()

    async def get_customers_details_by_user_id(db_obj: AsyncSession, user_id: UUID):
        """
        This function gets a customers_details from the database by using their user id.
        :param user_id: Id of the user.
        :param db_obj: Database session object
        """
        result = await db_obj.execute(
            select(CustomerDetails).where(CustomerDetails.user_id == user_id)
        )
        return result.scalars().all()
