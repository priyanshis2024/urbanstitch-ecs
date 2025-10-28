from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from src.dao.models.product import Subcategory
from src.dto.category import SubcategoryUpdate, SubcategoryCreate
from src.utils.constants import Status
from typing import Optional, List, Dict
from sqlalchemy import func, or_


class subcategory_dao:
    async def get_subcategory_by_id(subcategory_id: UUID, db_obj: AsyncSession):
        """
        This function gets a subcategory details from the database by using their subcategory id.
        :param subcategory_id: id of the subcategory.
        :param db_obj: AsyncSession: Pass the database asynchronous session object to the function
        """
        result = await db_obj.execute(
            select(Subcategory).filter(Subcategory.id == subcategory_id)
        )
        return result.scalars().first()

    async def get_subcategories_by_ids(
        db: AsyncSession, subcategory_ids: List[UUID]
    ) -> Dict[UUID, Subcategory]:
        result = await db.execute(
            select(Subcategory).where(Subcategory.id.in_(subcategory_ids))
        )
        subcategories = result.scalars().all()
        return {sub.id: sub for sub in subcategories}

    async def create_subcategory(subcategory: SubcategoryCreate, db_obj: AsyncSession):
        """
        This function creates a subcategory in the database.
        :param subcategory: Subcategory creation request payload schema.
        :param db_obj: database object
        """
        db_obj.add(subcategory)
        await db_obj.commit()
        await db_obj.refresh(subcategory)
        return subcategory

    async def delete_subcategory(subcategory: Subcategory, db_obj: AsyncSession):
        """
        This function deletes the subcategory details from the database.
        :param subcategory: subcategory payload.
        :param db_obj: database object
        """
        await db_obj.delete(subcategory)

    async def update_subcategory(
        db_obj: AsyncSession,
        subcategory_db: Subcategory,
        subcategory: SubcategoryUpdate,
    ):
        """
        This function update a subcategory details in the database.

        :param subcategory_db: Subcategory update request payload schema.
        :param db_obj: database object
        """
        for key, value in subcategory.dict(exclude_unset=True).items():
            setattr(subcategory_db, key, value)
        return subcategory_db

    async def update_subcategory_status(
        db_obj: AsyncSession, subcategory: Subcategory, new_status: Status
    ):
        """
        The update_subcategory_status function is used to update the status of subcategory for the given subcategory id.

        :param subcategory: Get the subcategory details
        :param new_status: Updated new subcategory status
        :param db_obj: database object
        """
        subcategory.status = new_status
        return subcategory

    async def all_subcategory(
        db_obj: AsyncSession,
        search: Optional[str] = None,
        sort_by: Optional[str] = "created_at",
        sort_order: Optional[str] = "asc",
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
    ):
        """
        Retrieves all subcategories with filtering, sorting, pagination, and total count.
        It takes in a number of parameters that are used to filter and sort the results.
        :param search: Used to searching
        :param sort_order: Determine if the query should be sorted in ascending or descending order
        :param sort_by: Sort the results by a particular column
        :param limit: Limit the number of results returned
        :param offset: Skip the first n records
        :param db_obj: database object
        """
        filters = []

        if search:
            filters.append(or_(Subcategory.name.ilike(f"%{search}%")))

        count_query = select(func.count()).select_from(Subcategory)
        if filters:
            count_query = count_query.where(*filters)

        count_result = await db_obj.execute(count_query)
        total_subcategories_count = count_result.scalar()

        query = select(Subcategory)
        if filters:
            query = query.where(*filters)

        if sort_by:
            if sort_order == "asc":
                query = query.order_by(getattr(Subcategory, sort_by).asc())
            elif sort_order == "desc":
                query = query.order_by(getattr(Subcategory, sort_by).desc())

        query = query.limit(limit).offset(offset)
        result = await db_obj.execute(query)

        return {
            "total_subcategories_count": total_subcategories_count,
            "subcategories": result.scalars().all(),
        }
