from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID, uuid4
from src.dao.models.product import Order, Product, Subproduct, OrderHistory
from src.dao.models.user import CustomerDetails
from src.dto.checkout import CartResponse
from src.dto.product import SubproductResponse
from datetime import datetime
from sqlalchemy.orm import selectinload
from src.utils.constants import UuidPrefix
from sqlalchemy import func
from typing import Optional
from src.utils.utils import attach_prefix_to_uuid, remove_prefix


class order_dao:
    async def create_order(order: Order, db_obj: AsyncSession):
        """
        Adds a new order to the database and commits it.
        """
        db_obj.add(order)
        await db_obj.commit()
        await db_obj.refresh(order)
        return order

    async def create_order_history(
        order_id: UUID,
        cart_item: CartResponse,
        subproduct: SubproductResponse,
        db_obj: AsyncSession,
    ):
        """
        Create an order history entry for a given order.
        """
        if subproduct.price is None:
            raise ValueError(f"Subproduct {cart_item.subproduct_id} has no price.")

        order_history = OrderHistory(
            id=uuid4(),
            order_id=order_id,
            subproduct_id=cart_item.subproduct_id,
            price=subproduct.price,
            order_quantity=cart_item.order_quantity,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db_obj.add(order_history)
        await db_obj.commit()
        await db_obj.refresh(order_history)

    async def get_order_detail_by_id(
        order_id: UUID, db_obj: AsyncSession
    ) -> Order | None:
        """
        Fetches a order by ID from the database.
        :param order_id: The ID of the order to retrieve
        :param db_obj: The async database session
        :return: Order instance or None
        """
        result = await db_obj.execute(
            select(Order)
            .filter(Order.id == order_id)
            .options(selectinload(Order.order_histories))
        )
        return result.scalars().first()

    async def get_order_by_order_id(order_id: UUID, db_obj: AsyncSession):
        """
        Fetches a order by ID from the database.
        """
        result = await db_obj.execute(
            select(Order)
            .options(
                selectinload(Order.order_histories).selectinload(
                    OrderHistory.subproducts
                ),
                selectinload(Order.payments),
            )
            .filter(Order.id == order_id)
        )
        order = result.scalars().first()

        if UuidPrefix.USER in order.user_id:
            user_id = remove_prefix(order.user_id)
            customer_id = remove_prefix(order.customer_id)
            customer_result = await db_obj.execute(
                select(CustomerDetails)
                .options(selectinload(CustomerDetails.users))
                .filter(
                    CustomerDetails.user_id == user_id,
                    CustomerDetails.id == customer_id,
                )
            )
            order.customer_details = customer_result.scalars().first()

        return order

    async def get_orders_by_user_id(user_id: str, db_obj: AsyncSession) -> list[Order]:
        user_id_str = attach_prefix_to_uuid(
            input_uuid=user_id, prefix=UuidPrefix.USER.value
        )
        result = await db_obj.execute(
            select(Order)
            .filter(Order.user_id == user_id_str)
            .options(selectinload(Order.order_histories))
        )
        return result.scalars().all()

    async def get_order_by_id(order_id: UUID, db_obj: AsyncSession):
        result = await db_obj.execute(select(Order).filter(Order.id == order_id))
        return result.scalars().first()

    async def get_order_by_id_with_details(order_id: UUID, db_obj: AsyncSession):
        result = await db_obj.execute(
            select(Order)
            .options(
                selectinload(Order.order_histories)
                .selectinload(OrderHistory.subproducts)
                .selectinload(Subproduct.products),
                selectinload(Order.payments),
            )
            .filter(Order.id == order_id)
        )
        return result.scalars().first()

    async def update_order_and_inventory_status(
        db_obj: AsyncSession,
        order: Order,
        subproducts: list[Subproduct],
        products: list[Product],
    ):
        db_obj.add(order)
        db_obj.add_all(subproducts)
        db_obj.add_all(products)

        await db_obj.commit()
        await db_obj.refresh(order)
        return order

    async def delete_order(order: Order, db_obj: AsyncSession):
        await db_obj.delete(order)

    async def all_order(
        db_obj: AsyncSession,
        search: Optional[str],
        limit: Optional[int],
        offset: Optional[int],
    ):
        """Function to fetch all order details."""
        filters = []

        if search:
            filters.append(Order.id.ilike(f"%{search}%"))

        count_query = select(func.count()).select_from(Order)
        if filters:
            count_query = count_query.where(*filters)
        count_result = await db_obj.execute(count_query)
        total_order_count = count_result.scalar()

        query = select(Order).options(selectinload(Order.order_histories))
        if filters:
            query = query.where(*filters)
        query = query.limit(limit).offset(offset)

        result = await db_obj.execute(query)
        orders = result.scalars().all()

        return total_order_count, orders
