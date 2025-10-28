from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from src.dao.models.product import Cart, Subproduct
from src.dto.checkout import (
    CartCreate,
    CartUpdate,
)
from sqlalchemy.orm import joinedload
from sqlalchemy import func, or_, delete
from typing import Optional, List
from src.utils.utils import attach_prefix_to_uuid
from src.utils.constants import UuidPrefix


class checkout_dao:
    async def get_cart_by_id(cart_id: UUID, db_obj: AsyncSession):
        result = await db_obj.execute(select(Cart).filter(Cart.id == cart_id))
        return result.scalars().first()

    async def create_cart(db_obj: AsyncSession, cart: CartCreate):
        """
        This function creates a cart details in the database.

        :param cart: cart creation request payload schema.
        :param db_obj: database object
        """
        db_obj.add(cart)
        await db_obj.commit()
        await db_obj.refresh(cart)
        return cart

    async def fetch_cart_product(
        db_obj: AsyncSession, subproduct_id: UUID, cart_id: UUID, user_id: str
    ):
        """
        This function checks a product from the database by using product id field.
        """
        query = select(Cart).filter(
            Cart.id == cart_id,
            Cart.subproduct_id == subproduct_id,
            Cart.user_id == user_id,
        )
        result = await db_obj.execute(query)
        return result.scalars().first()

    async def fetch_cart_with_details(db_obj: AsyncSession, cart_id: UUID):
        """
        Fetch cart with product and subproduct details using eager loading.
        """
        query = (
            select(Cart)
            .options(
                joinedload(Cart.subproducts),
                joinedload(Cart.subproducts).joinedload(Subproduct.products),
                joinedload(Cart.subproducts).joinedload(Subproduct.sizes),
            )
            .filter(Cart.id == cart_id)
        )
        result = await db_obj.execute(query)
        return result.scalars().first()

    async def update_cart(db_obj: AsyncSession, cart_db: Cart, cart: CartUpdate):
        for key, value in cart.dict(exclude_unset=True).items():
            setattr(cart_db, key, value)
        return cart_db

    async def get_all_carts_by_user_id(
        user_id: str, db_obj: AsyncSession
    ) -> list[Cart]:
        user_id_str = attach_prefix_to_uuid(
            input_uuid=user_id, prefix=UuidPrefix.USER.value
        )
        result = await db_obj.execute(select(Cart).where(Cart.user_id == user_id_str))
        return result.scalars().all()

    async def delete_cart(db_obj: AsyncSession, cart: Cart):
        await db_obj.delete(cart)

    async def delete_all_cart_items_by_user_id(user_id: str, db_obj: AsyncSession):
        await db_obj.execute(delete(Cart).where(Cart.user_id == user_id))

    async def all_cart(
        db_obj: AsyncSession,
        user_id: str,
        search: Optional[str] = None,
        sort_by: Optional[str] = "created_at",
        sort_order: Optional[str] = "asc",
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
    ) -> List[Cart]:
        """
        The all_cart function is used to retrieve all the cart in the database.
        It takes in a number of parameters that are used to filter and sort the results.
        :param search: Used to searching
        :param sort_order: Determine if the query should be sorted in ascending or descending order
        :param sort_by: Sort the results by a particular column
        :param limit: Limit the number of results returned
        :param offset: Skip the first n records
        :param db: database object

        :return: all cart by applying filter and sorting
        """
        temp_user = attach_prefix_to_uuid(
            input_uuid=user_id, prefix=UuidPrefix.USER.value
        )

        filters = [Cart.user_id == temp_user]
        if search:
            filters.append(
                or_(
                    Cart.user_id.ilike(f"%{search}%"),
                    Cart.order_quantity.ilike(f"%{search}%"),
                )
            )
        count_query = select(func.count()).select_from(Cart).where(*filters)
        count_result = await db_obj.execute(count_query)
        total_cart_product_count = count_result.scalar()

        query = (
            select(Cart)
            .options(joinedload(Cart.subproducts).joinedload(Subproduct.products))
            .options(joinedload(Cart.subproducts).joinedload(Subproduct.sizes))
            .where(*filters)
        )

        if sort_by:
            if sort_order == "asc":
                query = query.order_by(getattr(Cart, sort_by).asc())
            elif sort_order == "desc":
                query = query.order_by(getattr(Cart, sort_by).desc())

        query = query.limit(limit).offset(offset)
        result = await db_obj.execute(query)

        return {
            "total_cart_product_count": total_cart_product_count,
            "cart_products": result.scalars().all(),
        }

    async def get_cart_items_by_user_id(user_id: UUID, db_obj: AsyncSession):
        """
        Fetch cart items for the given user_id.
        """

        result = await db_obj.execute(select(Cart).filter(Cart.user_id == user_id))
        cart_items = result.scalars().all()

        if not cart_items:
            print(f"No cart items found for user_id: {user_id}")
        else:
            print(f"{len(cart_items)} cart items found for user_id: {user_id}")

        return cart_items
