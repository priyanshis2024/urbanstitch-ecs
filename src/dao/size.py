from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from src.dao.models.product import (
    Size,
    Subproduct,
    Product,
    Category,
    CategoryXref,
    Subcategory,
)
from src.dto.size import SizeCreate, SizeUpdate
from sqlalchemy import or_, func, distinct, and_
from typing import Optional, List


class size_dao:
    async def get_size_by_id(size_id: UUID, db_obj: AsyncSession):
        """
        This function gets a size details from the database by using their size id.
        :param size_id: id of the size.
        :param db_obj: AsyncSession: Pass the database asynchronous session object to the function
        """
        result = await db_obj.execute(select(Size).filter(Size.id == size_id))
        return result.scalars().first()

    async def get_sizes_by_ids(size_ids: List[UUID], db_obj: AsyncSession):
        query = select(Size).where(Size.id.in_(size_ids))
        result = await db_obj.execute(query)
        return result.scalars().all()

    async def fetch_size(db_obj: AsyncSession, size: str):
        """
        This function gets a size from the database by using size name field.
        :param db: AsyncSession: Pass the database asynchronous session object to the function
        """
        result = await db_obj.execute(select(Size).filter(Size.size == size))
        return result.scalars().first()

    async def create_sizes_bulk(
        db_obj: AsyncSession, sizes: List[SizeCreate]
    ) -> List[Size]:
        """
        This function creates a size in the database.

        :param size: SizeCreate creation request payload schema.
        :param db_obj: database object
        """
        db_obj.add_all(sizes)
        await db_obj.commit()
        for size in sizes:
            await db_obj.refresh(size)
        return sizes

    async def update_size(db_obj: AsyncSession, size_db: Size, size: SizeUpdate):
        """
        This function update a size details in the database.

        :param size_db: Size update request payload schema.
        :param db_obj: database object
        """
        for key, value in size.dict(exclude_unset=True).items():
            setattr(size_db, key, value)
        return size_db

    async def delete_size(db_obj: AsyncSession, size: Size):
        """
        This function deletes the size details from the database.
        :param size: size payload.
        :param db_obj: database object
        """
        await db_obj.delete(size)

    async def all_size(
        db_obj: AsyncSession,
        search: Optional[str] = None,
        sort_by: Optional[str] = "created_at",
        sort_order: Optional[str] = "asc",
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
    ):
        """
        The all_size function is used to retrieve all the sizes in the database.
        It takes in a number of parameters that are used to filter and sort the results.
        :param search: Used to searching
        :param sort_order: Determine if the query should be sorted in ascending or descending order
        :param sort_by: Sort the results by a particular column
        :param limit: Limit the number of results returned
        :param offset: Skip the first n records
        :param db_obj: database object

        :return: all size by applying filter and sorting
        """
        filters = []

        if search:
            filters.append(or_(Size.size.ilike(f"%{search}%")))

        count_query = select(func.count()).select_from(Size)
        if filters:
            count_query = count_query.where(*filters)

        count_result = await db_obj.execute(count_query)
        total_size_count = count_result.scalar()

        query = select(Size)
        if filters:
            query = query.where(*filters)

        if sort_by:
            if sort_order == "asc":
                query = query.order_by(getattr(Size, sort_by).asc())
            elif sort_order == "desc":
                query = query.order_by(getattr(Size, sort_by).desc())

        query = query.limit(limit).offset(offset)
        result = await db_obj.execute(query)

        return {"total_size_count": total_size_count, "sizes": result.scalars().all()}

    async def all_filtered_size(
        db_obj: AsyncSession,
        search: Optional[str],
        sort_by: Optional[str],
        sort_order: Optional[str],
        limit: Optional[int],
        offset: Optional[int],
        category_id: Optional[UUID] = None,
        subcategory_id: Optional[List[UUID]] = None,
    ):
        filters = []

        if search:
            filters.append(or_(Size.size.ilike(f"%{search}%")))

        count_query = select(func.count()).select_from(Size)
        if filters:
            count_query = count_query.where(*filters)

        count_result = await db_obj.execute(count_query)
        total_size_count = count_result.scalar()
        if category_id == None and subcategory_id == None:
            query = (
                select(Size)
                .join(Subproduct, Subproduct.size_id == Size.id)
                .join(Product, Subproduct.product_id == Product.id)
                .group_by(Size.id)
            )
        if category_id:
            query = (
                select(Size)
                .join(Subproduct, Subproduct.size_id == Size.id)
                .join(Product, Subproduct.product_id == Product.id)
                .join(CategoryXref, Product.category_xref_id == CategoryXref.id)
                .join(Category, CategoryXref.category_id == Category.id)
                .where(Category.id == category_id)
                .group_by(Size.id)
            )
        if subcategory_id:
            query = (
                select(Size)
                .join(Subproduct, Subproduct.size_id == Size.id)
                .join(Product, Subproduct.product_id == Product.id)
                .join(CategoryXref, Product.category_xref_id == CategoryXref.id)
                .join(Subcategory, CategoryXref.subcategory_id == Subcategory.id)
                .where(Subcategory.id.in_(subcategory_id))
                .group_by(Size.id)
            )
        if category_id and subcategory_id:
            query = (
                select(Size)
                .join(Subproduct, Subproduct.size_id == Size.id)
                .join(Product, Subproduct.product_id == Product.id)
                .join(CategoryXref, Product.category_xref_id == CategoryXref.id)
                .join(Category, CategoryXref.category_id == Category.id)
                .join(Subcategory, CategoryXref.subcategory_id == Subcategory.id)
                .where(
                    and_(Category.id == category_id, Subcategory.id.in_(subcategory_id))
                )
                .group_by(Size.id)
            )
        if filters:
            query = query.where(*filters)

        if sort_by:
            if sort_order == "asc":
                query = query.order_by(getattr(Size, sort_by).asc())
            elif sort_order == "desc":
                query = query.order_by(getattr(Size, sort_by).desc())

        query = query.limit(limit).offset(offset)
        result = await db_obj.execute(query)

        return {"total_size_count": total_size_count, "sizes": result.scalars().all()}
