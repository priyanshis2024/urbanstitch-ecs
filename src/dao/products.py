from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from src.dao.models.product import (
    Product,
    Subproduct,
    Size,
    Category,
    Subcategory,
    CategoryXref,
    Review,
)
from src.dto.product import (
    ProductCreate,
    ProductUpdate,
)
from sqlalchemy import or_, func, and_
from typing import Optional, List
from sqlalchemy.orm import selectinload
from src.utils.constants import Status

# from src.utils.utils import get_similar_words_with_sbert


class product_dao:
    async def get_product_by_id(
        product_id: UUID, db_obj: AsyncSession
    ) -> Product | None:
        """
        Fetches a product by ID from the database.
        :param product_id: The ID of the product to retrieve
        :param db_obj: The async database session
        :return: Product instance or None
        """
        result = await db_obj.execute(
            select(Product)
            .filter(Product.id == product_id)
            .options(selectinload(Product.subproducts).selectinload(Subproduct.sizes))
        )
        return result.scalars().first()

    async def get_products_by_ids(db: AsyncSession, product_ids: List[UUID]):
        result = await db.execute(select(Product.id).where(Product.id.in_(product_ids)))
        return result.scalars().all()

    async def get_product(product_id: UUID, db_obj: AsyncSession):
        """
        Fetches a product by ID from the database.
        :param product_id: The ID of the product to retrieve
        :param db_obj: The async database session
        :return: Product
        """
        result = await db_obj.execute(select(Product).filter(Product.id == product_id))
        return result.scalars().first()

    async def calculate_average_product_rating(db_obj: AsyncSession, product_id: UUID):
        result = await db_obj.execute(
            select(func.avg(Review.rating)).filter(Review.product_id == product_id)
        )
        return result.scalar()

    async def create_product(db_obj: AsyncSession, product: ProductCreate):
        db_obj.add(product)
        await db_obj.commit()
        await db_obj.refresh(product)
        return product

    async def update_product(
        db_obj: AsyncSession, product_db: Product, product: ProductUpdate
    ):
        """
        This function update a product details in the database.

        :param product: product update request payload schema.
        :param product_db: product update request payload schema.
        :param db_obj: database object
        """
        for key, value in product.dict(exclude_unset=True).items():
            setattr(product_db, key, value)
        return product_db

    async def delete_product(db_obj: AsyncSession, product: Product):
        await db_obj.delete(product)

    async def all_products(
        db_obj: AsyncSession,
        search: Optional[str] = None,
        sort_by: Optional[str] = "created_at",
        sort_order: Optional[str] = "asc",
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
        min_rating: Optional[int] = None,
        max_rating: Optional[int] = None,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        color: Optional[List[str]] = None,
        size: Optional[List[UUID]] = None,
        category: Optional[UUID] = None,
        subcategory: Optional[List[UUID]] = None,
        status: Optional[List[int]] = None,
    ):
        """
        Retrieves products with filtering, sorting, pagination, and total count.
        """
        filters = []

        if search:
            # TODO: Add the ML functionality for the searching
            # similar_words = await get_similar_words_with_sbert(search)
            # search_terms = [search] + similar_words

            # filter_conditions = []
            # for term in search_terms:
            #     filter_conditions.append(Product.name.ilike(f"%{term}%"))
            #     filter_conditions.append(Product.description.ilike(f"%{term}%"))
            #     filter_conditions.append(Product.fabric.ilike(f"%{term}%"))
            # filters.append(or_(*filter_conditions))

            filters.append(
                or_(
                    Product.name.ilike(f"%{search}"),
                    Product.description.ilike(f"%{search}%"),
                    Product.fabric.ilike(f"%{search}%"),
                )
            )

        if min_rating is not None:
            filters.append(Product.rating >= min_rating)
        if max_rating is not None:
            filters.append(Product.rating <= max_rating)
        if min_price is not None:
            filters.append(Subproduct.price >= min_price)
        if max_price is not None:
            filters.append(Subproduct.price <= max_price)
        if color:
            if isinstance(color, List):
                filters.append(Subproduct.color.in_(color))
            else:
                filters.append(Subproduct.color == color)
        if size:
            if isinstance(size, List):
                filters.append(Size.id.in_(size))
            else:
                filters.append(Size.id == size)
        if status:
            if isinstance(status, List):
                filters.append(Subproduct.status.in_(status))
            else:
                filters.append(Subproduct.status == status)
        if category:
            filters.append(Category.id == category)
        if subcategory:
            if isinstance(subcategory, List):
                filters.append(Subcategory.id.in_(subcategory))
            else:
                filters.append(Subcategory.id == subcategory)
        count_query = select(func.count()).select_from(Product)
        if filters:
            count_query = count_query.where(and_(*filters))

        count_result = await db_obj.execute(count_query)
        total_count = count_result.scalar()

        query = (
            select(Product)
            .options(selectinload(Product.subproducts).selectinload(Subproduct.sizes))
            .outerjoin(Subproduct)
            .outerjoin(Size, Size.id == Subproduct.size_id)
            .outerjoin(CategoryXref, Product.category_xref_id == CategoryXref.id)
            .outerjoin(Category, CategoryXref.category_id == Category.id)
            .outerjoin(Subcategory, CategoryXref.subcategory_id == Subcategory.id)
            .group_by(Product.id)
        )

        if filters:
            query = query.where(and_(*filters))

        if sort_by:
            order_column = getattr(Product, sort_by, None)
            query = query.order_by(
                order_column.asc() if sort_order == "asc" else order_column.desc()
            )

        query = query.limit(limit).offset(offset)
        result = await db_obj.execute(query)

        return {"total_count": total_count, "products": result.scalars().unique().all()}

    async def update_product_status(
        db_obj: AsyncSession, product: Product, new_status: Status
    ):
        """
        The update_product_status function is used to update the status of product for the given product id.

        :param product: Get the product details
        :param new_status: Updated new product status
        :param db_obj: database object
        """
        product.status = new_status
        return product
