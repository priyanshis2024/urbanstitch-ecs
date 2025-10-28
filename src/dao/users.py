from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.dao.models.user import User
from src.dto.user import UserCreate, UserUpdate
from uuid import UUID
from src.utils.constants import Status
from typing import Optional
from sqlalchemy import or_, asc, desc, func
from src.dao.models.user import User


class user_dao:
    async def get_user(user_id: UUID, db_obj: AsyncSession):
        """
        This function gets a user details from the database by using their user id.
        :param user_id: id of the user.
        :param db_obj: AsyncSession: Pass the database asynchronous session object to the function
        """
        result = await db_obj.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()

    async def fetch_email_detail(db_obj: AsyncSession, email: str):
        """
        This function gets a email from the database by using email field.
        :param db: AsyncSession: Pass the database asynchronous session object to the function
        """
        result = await db_obj.execute(select(User).filter(User.email == email))
        return result.scalars().first()

    async def create_user(db_obj: AsyncSession, user: UserCreate):
        """
        This function creates a user in the database.

        :param user: User creation request payload schema.
        :param db_obj: database object
        """
        db_obj.add(user)
        await db_obj.commit()
        await db_obj.refresh(user)
        return user

    async def update_user(db_obj: AsyncSession, user_db: User, user: UserUpdate):
        """
        This function update a user details in the database.

        :param user_db: User update request payload schema.
        :param db_obj: database object
        """
        for key, value in user.dict(exclude_unset=True).items():
            setattr(user_db, key, value)
        return user_db

    async def delete_user(db_obj: AsyncSession, user: User):
        """
        This function deletes the user details from the database.
        :param user: user payload.
        :param db_obj: database object
        """
        await db_obj.delete(user)

    async def all_user(
        db_obj: AsyncSession,
        search: Optional[str] = None,
        sort_by: Optional[str] = "created_at",
        sort_order: Optional[str] = "asc",
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
    ):
        """
        Retrieves all users with filtering, sorting, pagination, and total count.
        It takes in a number of parameters that are used to filter and sort the results.
        :param search: Used to searching
        :param sort_order: Determine if the query should be sorted in ascending or descending order
        :param sort_by: Sort the results by a particular column
        :param limit: Limit the number of results returned
        :param offset: Skip the first n records
        :param db: database object
        """
        filters = []

        if search:
            filters.append(
                or_(
                    User.email.ilike(f"%{search}%"),
                    User.first_name.ilike(f"%{search}%"),
                    User.last_name.ilike(f"%{search}%"),
                    User.username.ilike(f"%{search}%"),
                )
            )

        count_query = select(func.count()).select_from(User)
        if filters:
            count_query = count_query.where(*filters)

        count_result = await db_obj.execute(count_query)
        total_user_count = count_result.scalar()

        query = select(User)
        if filters:
            query = query.where(*filters)

        if sort_by:
            if sort_order == "asc":
                query = query.order_by(getattr(User, sort_by).asc())
            elif sort_order == "desc":
                query = query.order_by(getattr(User, sort_by).desc())

        query = query.limit(limit).offset(offset)
        result = await db_obj.execute(query)

        return {"total_user_count": total_user_count, "users": result.scalars().all()}

    async def update_status(db_obj: AsyncSession, user: User, new_status: Status):
        """
        The update_status function is used to update the status of user for the given user id.

        :param user: Get the user details
        :param new_status: Updated new user status
        :param db_obj: database object
        """
        user.status = new_status
        return user
