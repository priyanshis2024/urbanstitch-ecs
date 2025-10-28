from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from src.dao.models.product import Wishlist, Subproduct
from src.dto.wishlist import (
    WishlistCreate,
)
from sqlalchemy.orm import joinedload
from sqlalchemy import or_, func
from typing import Optional, List
from src.utils.constants import UuidPrefix
from src.utils.utils import attach_prefix_to_uuid


class wishlist_dao:
    async def get_wishlist_by_id(wishlist_id: UUID, db_obj: AsyncSession):
        result = await db_obj.execute(
            select(Wishlist).filter(Wishlist.id == wishlist_id)
        )
        return result.scalars().first()

    async def create_wishlist(db_obj: AsyncSession, wishlist: WishlistCreate):
        """
        This function creates a wishlist in the database.
        :param wishlist: Wishlist creation request payload schema.
        :param db: database object
        """
        db_obj.add(wishlist)
        await db_obj.commit()
        await db_obj.refresh(wishlist)
        return wishlist

    async def fetch_wishlist_product(
        db_obj: AsyncSession, subproduct_id: UUID, wishlist_id: UUID, user_id: str
    ):
        """
        This function checks a product from the database by using subproduct id field.
        :param db: AsyncSession: Pass the database asynchronous session object to the function
        """
        result = await db_obj.execute(
            select(Wishlist).filter(
                Wishlist.id == wishlist_id,
                Wishlist.subproduct_id == subproduct_id,
                Wishlist.user_id == user_id,
            )
        )
        return result.scalars().first()

    async def fetch_wishlist_with_details(db_obj: AsyncSession, wishlist_id: UUID):
        """
        Fetch wishlist with product and subproduct details.
        """
        query = (
            select(Wishlist)
            .options(joinedload(Wishlist.subproducts).joinedload(Subproduct.products))
            .filter(Wishlist.id == wishlist_id)
        )
        result = await db_obj.execute(query)
        return result.scalars().first()

    async def delete_wishlist(db_obj: AsyncSession, wishlist: Wishlist):
        await db_obj.delete(wishlist)

    async def get_all_wishlist_details(
        db_obj: AsyncSession,
        user_id: str,
        search: Optional[str] = None,
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
    ) -> List[Wishlist]:
        """
        Fetch all wishlist items for a specific user with product and subproduct details.
        """
        temp_user = attach_prefix_to_uuid(
            input_uuid=user_id, prefix=UuidPrefix.USER.value
        )

        filters = [Wishlist.user_id == temp_user]

        if search:
            filters.append(
                or_(
                    Wishlist.user_id.ilike(f"%{search}%"),
                    Wishlist.subproduct_id.ilike(f"%{search}%"),
                )
            )

        count_query = select(func.count()).select_from(Wishlist).where(*filters)
        count_result = await db_obj.execute(count_query)
        total_wishlist_product_count = count_result.scalar()

        query = (
            select(Wishlist)
            .options(joinedload(Wishlist.subproducts).joinedload(Subproduct.products))
            .where(*filters)
            .limit(limit)
            .offset(offset)
        )

        result = await db_obj.execute(query)

        return {
            "total_wishlist_product_count": total_wishlist_product_count,
            "wishlist_products": result.scalars().all(),
        }
