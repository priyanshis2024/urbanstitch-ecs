from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from src.dao.models.product import Category, Subcategory, CategoryXref
from src.dto.category import CategoryUpdate, CategoryCreate
from sqlalchemy import func, or_
from typing import Optional, List
from src.utils.constants import Status
from datetime import datetime


class category_dao:
    async def get_category_by_id(category_id: UUID, db_obj: AsyncSession):
        """
        This function gets a category details from the database by using their category id.
        :param category_id: id of the category.
        :param db_obj: AsyncSession: Pass the database asynchronous session object to the function
        """
        result = await db_obj.execute(
            select(Category).filter(Category.id == category_id)
        )
        return result.scalars().first()

    async def get_categories_by_ids(db: AsyncSession, category_ids: List[UUID]):
        result = await db.execute(
            select(Category.id).where(Category.id.in_(category_ids))
        )
        return set(result.scalars().all())

    async def get_category(category_id: UUID, db_obj: AsyncSession):
        query = (
            select(Category, Subcategory)
            .join(CategoryXref, Category.id == CategoryXref.category_id)
            .join(Subcategory, Subcategory.id == CategoryXref.subcategory_id)
            .filter(Category.id == category_id)
        )
        result = await db_obj.execute(query)
        data = result.all()

        if not data:
            return None

        category = data[0][0]
        subcategories = [row[1] for row in data]

        return category, subcategories

    async def create_category(category: CategoryCreate, db_obj: AsyncSession):
        """
        This function creates a category in the database.
        :param category: Category creation request payload schema.
        :param db_obj: database object
        """
        db_obj.add(category)
        await db_obj.commit()
        await db_obj.refresh(category)
        return category

    async def update_category(
        db_obj: AsyncSession, category_db: Category, category: CategoryUpdate
    ):
        """
        This function update a category details in the database.

        :param category_db: Category update request payload schema.
        :param db_obj: database object
        """
        category_db.updated_at = datetime.now()
        for key, value in category.dict(exclude_unset=True).items():
            setattr(category_db, key, value)
        return category_db

    async def delete_category(category: Category, db_obj: AsyncSession):
        """
        This function deletes the category details from the database.
        :param category: category payload.
        :param db_obj: database object
        """
        await db_obj.delete(category)

    async def all_category(
        db_obj: AsyncSession,
        search: Optional[str] = None,
        sort_by: Optional[str] = "created_at",
        sort_order: Optional[str] = "asc",
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
    ):
        """
        Retrieves all categories with filtering, sorting, pagination, and total count.
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
            filters.append(or_(Category.name.ilike(f"%{search}%")))

        count_query = select(func.count()).select_from(Category)
        if filters:
            count_query = count_query.where(*filters)

        count_result = await db_obj.execute(count_query)
        total_categories_count = count_result.scalar()

        query = select(Category)
        if filters:
            query = query.where(*filters)

        if sort_by:
            if sort_order == "asc":
                query = query.order_by(getattr(Category, sort_by).asc())
            elif sort_order == "desc":
                query = query.order_by(getattr(Category, sort_by).desc())

        query = query.limit(limit).offset(offset)
        result = await db_obj.execute(query)

        return {
            "total_categories_count": total_categories_count,
            "categories": result.scalars().all(),
        }

    async def update_category_status(
        db_obj: AsyncSession, category: Category, new_status: Status
    ):
        """
        The update_category_status function is used to update the status of category for the given category id.

        :param category: Get the category details
        :param new_status: Updated new category status
        :param db_obj: database object
        """
        category.status = new_status
        return category
