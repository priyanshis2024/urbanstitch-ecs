from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.dao.models.user import UserRole
from src.dto.user_role import UserRoleCreate, UserRoleUpdate
from typing import Optional
from src.dao.models.user import UserRole
from sqlalchemy import or_


class user_role_dao:
    async def get_user_role(user_role_id: int, db_obj: AsyncSession):
        """
        This function gets a user role details from the database by using their user role id.
        :param user_role_id: Id of the user role.
        :param db_obj: AsyncSession: Pass the database asynchronous session object to the function
        """
        result = await db_obj.execute(
            select(UserRole).where(UserRole.id == user_role_id)
        )
        return result.scalars().first()

    async def create_user_role(db_obj: AsyncSession, user_role: UserRoleCreate):
        """
        This function creates a user role in the database.
        :param user_role: User role creation request payload schema.
        :param db_obj: database object
        """
        db_obj.add(user_role)
        await db_obj.commit()
        await db_obj.refresh(user_role)
        return user_role

    async def update_user_role(
        db_obj: AsyncSession, user_role_db: UserRole, user_role: UserRoleUpdate
    ):
        """
        This function update a user role details in the database.

        :param user_role_db: Database of the user role to be updated.
        :param user_role_id: Id of the user role to be updated .
        :param db_obj: database object
        """
        for key, value in user_role.dict(exclude_unset=True).items():
            setattr(user_role_db, key, value)
        return user_role_db

    async def delete_user_role(db_obj: AsyncSession, user_role: UserRole):
        """
        This function deletes the user role details from the database.
        :param user_role: Database of the user role to be deleted.
        :param db_obj: database object
        """
        await db_obj.delete(user_role)

    async def all_user_role(
        db_obj: AsyncSession,
        search: Optional[str] = None,
        sort_by: Optional[str] = "created_at",
        sort_order: Optional[str] = "asc",
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
    ):
        """
        The all_user_role function is used to retrieve all user roles in the database.
        It takes in parameters for limiting and offsetting the results.
        :param limit: Limit the number of results returned
        :param offset: Skip the first n records
        :param db_obj: database object

        :return: All user roles with pagination
        """
        filters = []

        if search:
            filters.append(or_(UserRole.role.ilike(f"%{search}%")))

        query = select(UserRole)
        if filters:
            query = query.where(*filters)

        if sort_by:
            if sort_order == "asc":
                query = query.order_by(getattr(UserRole, sort_by).asc())
            elif sort_order == "desc":
                query = query.order_by(getattr(UserRole, sort_by).desc())

        query = query.limit(limit).offset(offset)
        result = await db_obj.execute(query)
        return result.scalars().all()
