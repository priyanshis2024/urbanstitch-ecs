from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from src.dao.models.product import (
    Subproduct,
    Product,
    Size,
    Category,
    Subcategory,
    CategoryXref,
)
from src.dto.subproduct import SubproductCreate, SubproductUpdate
from sqlalchemy import asc, desc, or_, func, and_
from typing import Optional, List
from sqlalchemy.orm import selectinload
from src.utils.constants import Status

# from src.utils.utils import get_similar_words_with_sbert


class subproduct_dao:
    async def get_subproduct_by_id(subproduct_id: UUID, db_obj: AsyncSession):
        result = await db_obj.execute(
            select(Subproduct).filter(Subproduct.id == subproduct_id)
        )
        return result.scalars().first()

    async def get_subproducts_by_ids(subproduct_ids: List[UUID], db_obj: AsyncSession):
        query = select(Subproduct).where(Subproduct.id.in_(subproduct_ids))
        result = await db_obj.execute(query)
        return result.scalars().all()

    async def create_subproduct(db_obj: AsyncSession, subproduct: SubproductCreate):
        db_obj.add(subproduct)
        await db_obj.commit()
        await db_obj.refresh(subproduct)
        return subproduct

    async def create_bulk_subproduct(
        db_obj: AsyncSession, subproducts: List[SubproductCreate]
    ):
        """
        Create multiple subproducts in the database.
        """
        db_obj.add_all(subproducts)
        await db_obj.commit()
        for subproduct in subproducts:
            await db_obj.refresh(subproduct)
        return subproducts

    async def delete_subproduct(db_obj: AsyncSession, subproduct: Subproduct):
        await db_obj.delete(subproduct)

    async def update_subproduct(
        db_obj: AsyncSession,
        subproduct_db: Subproduct,
        subproduct: SubproductUpdate,
    ):
        for key, value in subproduct.dict(exclude_unset=True).items():
            setattr(subproduct_db, key, value)
        return subproduct_db

    async def fetch_single_subproduct_detail(subproduct_id: UUID, db_obj: AsyncSession):
        """
        Retrieves a single subproduct with its related product details.
        """
        query = (
            select(Subproduct)
            # .options(selectinload(Subproduct.products))
            .options(
                selectinload(Subproduct.sizes),
                selectinload(Subproduct.products)
                .selectinload(Product.category_xrefs)
                .selectinload(CategoryXref.categories),
                selectinload(Subproduct.products)
                .selectinload(Product.category_xrefs)
                .selectinload(CategoryXref.subcategories),
            )
            .outerjoin(Product, Product.id == Subproduct.product_id)
            .outerjoin(Size, Size.id == Subproduct.size_id)
            .where(Subproduct.id == subproduct_id)
        )
        result = await db_obj.execute(query)
        return result.scalars().first()

    async def all_subproduct_fetching_detail(
        db_obj: AsyncSession,
        search: Optional[str] = None,
        sort_by: Optional[str] = "created_at",
        sort_order: Optional[str] = "asc",
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        color: Optional[List[str]] = None,
        size: Optional[List[UUID]] = None,
        category: Optional[UUID] = None,
        subcategory: Optional[List[UUID]] = None,
        status: Optional[List[int]] = None,
        min_rating: Optional[float] = None,
        max_rating: Optional[float] = None,
    ):
        """
        Retrieves subproducts with filtering, sorting, pagination, and total count.
        """
        filters = []

        if search:
            # TODO: Add the ML functionality for the searching
            # similar_words = await get_similar_words_with_sbert(search)
            # search_terms = [search] + similar_words

            # filter_conditions = []
            # for term in search_terms:
            # filter_conditions.append(Product.name.ilike(f"%{term}%"))
            # filter_conditions.append(Product.description.ilike(f"%{term}%"))
            # filter_conditions.append(Product.fabric.ilike(f"%{term}%"))

            # filters.append(or_(*filter_conditions))

            filters.append(
                or_(
                    Product.name.ilike(f"%{search}"),
                    Product.description.ilike(f"%{search}%"),
                    Product.fabric.ilike(f"%{search}%"),
                )
            )

        if min_price is not None:
            filters.append(Subproduct.price >= min_price)
        if max_price is not None:
            filters.append(Subproduct.price <= max_price)
        if color:
            if isinstance(color, List):
                color_filters = [Subproduct.color.ilike(f"%{c}%") for c in color]
                filters.append(or_(*color_filters))
            else:
                filters.append(Subproduct.color.ilike(f"%{color}%"))

        if min_rating is not None:
            filters.append(Product.rating >= min_rating)
        if max_rating is not None:
            filters.append(Product.rating <= max_rating)
        if status is not None:
            if isinstance(status, List):
                filters.append(Subproduct.status.in_(status))
            else:
                filters.append(Subproduct.status == status)
        if size:
            if isinstance(size, List):
                filters.append(Subproduct.size_id.in_(size))
            else:
                filters.append(Subproduct.size_id == size)
        if category:
            filters.append(Category.id == category)

        if subcategory:
            if isinstance(subcategory, List):
                filters.append(Subcategory.id.in_(subcategory))
            else:
                filters.append(Subcategory.id == subcategory)

        count_query = (
            select(func.count())
            .select_from(Subproduct)
            .join(Product, Product.id == Subproduct.product_id)
            .join(CategoryXref, Product.category_xref_id == CategoryXref.id)
            .join(Category, CategoryXref.category_id == Category.id)
            .join(Subcategory, CategoryXref.subcategory_id == Subcategory.id)
        )

        if filters:
            count_query = count_query.where(and_(*filters))

        count_result = await db_obj.execute(count_query)
        total_subproduct_count = count_result.scalar()

        query = (
            select(Subproduct)
            .options(
                selectinload(Subproduct.products)
                .selectinload(Product.category_xrefs)
                .selectinload(CategoryXref.categories),
                selectinload(Subproduct.products)
                .selectinload(Product.category_xrefs)
                .selectinload(CategoryXref.subcategories),
            )
            .outerjoin(Product, Product.id == Subproduct.product_id)
            .outerjoin(Size, Size.id == Subproduct.size_id)
            .outerjoin(CategoryXref, Product.category_xref_id == CategoryXref.id)
            .outerjoin(Category, CategoryXref.category_id == Category.id)
            .outerjoin(Subcategory, CategoryXref.subcategory_id == Subcategory.id)
            # .distinct(Subproduct.product_id)
            # .order_by(Subproduct.product_id)
        )

        if filters:
            query = query.where(and_(*filters))

        if sort_by:
            order_column = getattr(Subproduct, sort_by, None) or getattr(
                Product, sort_by, None
            )
            if order_column:
                query = query.order_by(
                    order_column.asc() if sort_order == "asc" else order_column.desc()
                )

        query = query.limit(limit).offset(offset)
        result = await db_obj.execute(query)

        return {
            "total_subproduct_count": total_subproduct_count,
            "subproducts": result.scalars().unique().all(),
        }

    async def update_subproduct_status(
        db_obj: AsyncSession, subproduct: Subproduct, new_status: Status
    ):
        """
        The update_subproduct_status function is used to update the status of subproduct for the given subproduct id.

        :param subproduct: Get the subproduct details
        :param new_status: Updated new subproduct status
        :param db_obj: database object
        """
        subproduct.status = new_status
        return subproduct
