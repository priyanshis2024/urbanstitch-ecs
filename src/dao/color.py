from src.dao.models.product import (
    Product,
    Subproduct,
    Category,
    Subcategory,
    CategoryXref,
)
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import func, distinct
from sqlalchemy.future import select


class color_dao:

    async def all_distinct_color(
        db_obj: AsyncSession,
        search: Optional[str],
        limit: Optional[int],
        offset: Optional[int],
        category_id: Optional[UUID] = None,
        subcategory_id: Optional[List[UUID]] = None,
    ):
        filters = []

        if search:
            filters.append(Subproduct.color.ilike(f"%{search}%"))

        query = (
            select(func.array_agg(distinct(Subproduct.color)))
            .select_from(Product)
            .join(Subproduct, Subproduct.product_id == Product.id)
            .join(CategoryXref, Product.category_xref_id == CategoryXref.id)
        )

        if category_id:
            query = query.join(Category, CategoryXref.category_id == Category.id).where(
                Category.id == category_id
            )
        if subcategory_id:
            query = query.join(
                Subcategory, CategoryXref.subcategory_id == Subcategory.id
            ).where(Subcategory.id.in_(subcategory_id))
        if filters:
            query = query.where(*filters)

        query = query.limit(limit).offset(offset)
        result = await db_obj.execute(query)

        return result.scalar()
