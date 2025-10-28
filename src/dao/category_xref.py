from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import Optional
from src.dao.models.product import Subcategory, CategoryXref
from src.dto.category_xref import CategoryXrefCreate
from sqlalchemy import delete
from typing import List


class category_xref_dao:
    async def create_category_xref(
        category_xref: CategoryXrefCreate, db_obj: AsyncSession
    ):
        """
        This function creates a category_xref in the database.
        :param category_xref: CategoryXref creation request payload schema.
        :param db_obj: database object
        """
        db_obj.add(category_xref)
        await db_obj.commit()
        await db_obj.refresh(category_xref)
        return category_xref

    async def get_subcategories_by_category_id(db_obj: AsyncSession, category_id: UUID):
        result = await db_obj.execute(
            select(Subcategory)
            .join(CategoryXref, CategoryXref.subcategory_id == Subcategory.id)
            .filter(CategoryXref.category_id == category_id)
        )
        return result.scalars().all()

    async def get_subcategory_ids_by_category_id(
        db_obj: AsyncSession, category_id: UUID
    ):
        """
        Fetch all subcategory IDs associated with the given category ID.

        :param db_obj: AsyncSession object for DB transactions
        :param category_id: UUID of the category
        :return: List of subcategory UUIDs
        """
        result = await db_obj.execute(
            select(CategoryXref.subcategory_id).where(
                CategoryXref.category_id == str(category_id)
            )
        )
        return result.scalars().all()

    async def delete_category_xrefs_category_id_or_subcategory_id(
        db_obj: AsyncSession,
        category_id: Optional[UUID] = None,
        subcategory_id: Optional[UUID] = None,
    ):
        """
        Delete category-subcategory mappings using optional filters.

        :param db_obj: AsyncSession object for DB transactions
        :param category_id: Optional UUID of the category
        :param subcategory_id: Optional UUID of the subcategory
        :return: List of CategoryXref objects
        """
        query = delete(CategoryXref)

        if category_id and subcategory_id:
            query = query.where(
                CategoryXref.category_id == category_id,
                CategoryXref.subcategory_id == subcategory_id,
            )

        elif category_id:
            query = query.where(CategoryXref.category_id == category_id)
        await db_obj.execute(query)

    async def get_category_xref(
        db_obj: AsyncSession,
        category_id: Optional[UUID] = None,
        subcategory_id: Optional[UUID] = None,
    ) -> list[CategoryXref]:
        """
        Fetch category-subcategory mappings using optional filters.

        :param db_obj: AsyncSession object for DB transactions
        :param category_id: Optional UUID of the category
        :param subcategory_id: Optional UUID of the subcategory
        :return: List of CategoryXref objects
        """
        query = select(CategoryXref)

        if category_id and subcategory_id:
            query = query.where(
                CategoryXref.category_id == category_id,
                CategoryXref.subcategory_id == subcategory_id,
            )
        elif category_id:
            query = query.where(CategoryXref.category_id == category_id)
        elif subcategory_id:
            query = query.where(CategoryXref.subcategory_id == subcategory_id)

        result = await db_obj.execute(query)
        return result.scalars().all()

    async def get_subcategories_from_category_xref_by_category_id(
        db_obj: AsyncSession, category_id: UUID
    ):
        result = await db_obj.execute(
            select(CategoryXref, Subcategory)
            .join(CategoryXref, CategoryXref.subcategory_id == Subcategory.id)
            .filter(CategoryXref.category_id == category_id)
        )
        return result.all()
