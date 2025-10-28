from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
import stripe
from src.service.order_converter import Converter
from src.dao.db import transaction
from src.dao.models.product import Order
from src.dao.order import order_dao
from src.dao.checkout import checkout_dao
from src.dao.subproduct import subproduct_dao
from src.dao.payment import payment_dao
from src.dao.customer_details import customer_detail_dao
from src.dto.order import (
    UserOrderSummaryResponse,
)
from src.dto.payment import PaymentRefundUpdate
from src.utils.user_id import ADMIN_USER_ID
from src.exceptions.user import UnauthorizedUser
from src.exceptions.checkout import EmptyCartError
from src.exceptions.subproduct import SubproductNotFound
from src.exceptions.order import OrderNotFound, UserOrderNotFound
from datetime import datetime
from uuid import uuid4, UUID
from src.utils.constants import (
    UuidPrefix,
    OrderStatus,
    ErrorMessage,
    PaymentStatus,
    StripeStatus,
)
from src.utils.utils import attach_prefix_to_uuid, remove_prefix
from src.dto.common import Json_pagination
from src.middleware.logger import logger
from src.utils.email_sender import send_order_email
from src.utils.order_template import order_email_template


class OrderService:
    @transaction
    async def create_order(
        self, user_id: UUID, customer_id: UUID, db_obj: AsyncSession
    ):
        user_id_str = (
            attach_prefix_to_uuid(input_uuid=user_id, prefix=UuidPrefix.USER.value)
            if not str(user_id).startswith(UuidPrefix.USER.value)
            else str(user_id)
        )

        customer_id_str = (
            attach_prefix_to_uuid(
                input_uuid=customer_id, prefix=UuidPrefix.CUSTOMER.value
            )
            if not str(customer_id).startswith(UuidPrefix.CUSTOMER.value)
            else str(customer_id)
        )

        if str(user_id) == ADMIN_USER_ID or str(user_id).endswith(str(ADMIN_USER_ID)):
            logger.error(
                f"Unauthorized user. User with id '{user_id}' is not authorized user to access this resource."
            )
            raise UnauthorizedUser(
                user_id=user_id,
                message=ErrorMessage.UNAUTHORIZED_USER.format(user_id=user_id),
            )

        cart_items = await checkout_dao.get_cart_items_by_user_id(
            user_id=user_id_str, db_obj=db_obj
        )
        if not cart_items:
            logger.error(
                "Order creation failed: Please add items before placing an order."
            )
            raise EmptyCartError(message=ErrorMessage.EMPTY_CART_FOUND.format())

        order = Order(
            id=uuid4(),
            user_id=user_id_str,
            customer_id=customer_id_str,
            order_status=OrderStatus.PENDING,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        await order_dao.create_order(order, db_obj)

        for item in cart_items:
            subproduct = await subproduct_dao.get_subproduct_by_id(
                subproduct_id=item.subproduct_id, db_obj=db_obj
            )
            if not subproduct:
                logger.error(
                    f"Subproduct with id '{item.subproduct_id}' not found in the system."
                )
                raise SubproductNotFound(
                    subproduct_id=item.subproduct_id,
                    message=ErrorMessage.SUBPRODUCT_NOT_FOUND.format(
                        subproduct_id=item.subproduct_id
                    ),
                )

            await order_dao.create_order_history(
                order_id=order.id,
                cart_item=item,
                subproduct=subproduct,
                db_obj=db_obj,
            )
        await checkout_dao.delete_all_cart_items_by_user_id(
            user_id=user_id_str, db_obj=db_obj
        )

        order_response = await order_dao.get_order_detail_by_id(order.id, db_obj)

        return Converter.user_order_creation_dto_to_db(order_response)

    async def get_order_details_by_order_id(self, order_id: UUID, db_obj: AsyncSession):
        """
        Service function for the fetching all order details for the individual order.
        :param order_id: The ID of the order
        :param db_obj: The session object
        """
        order = await order_dao.get_order_by_order_id(order_id=order_id, db_obj=db_obj)
        if not order:
            logger.error(f"Order with id '{order_id}' not found in the system.")
            raise OrderNotFound(
                order_id=order_id,
                message=ErrorMessage.ORDER_NOT_FOUND.format(order_id=order_id),
            )
        return Converter.order_summary_db_to_dto(order)

    async def get_all_orders_by_user_id(self, user_id: UUID, db_obj: AsyncSession):
        """
        Service function for the fetching all order details for the user.
        :param user_id: The ID of the user
        :param db_obj: The session object
        """
        orders = await order_dao.get_orders_by_user_id(user_id=user_id, db_obj=db_obj)
        if not orders:
            logger.error(f"Order with user id '{user_id}' not found in the system.")
            raise UserOrderNotFound(
                user_id=user_id,
                message=ErrorMessage.USER_ORDER_NOT_FOUND.format(user_id=user_id),
            )
        return [Converter.order_response_db_to_dto(order) for order in orders]

    @transaction
    async def delete_order(self, id: UUID, db_obj: AsyncSession):
        """
        Service function to delete an order asynchronously.
        :param db_obj: The session object
        :param id: The ID of the order to delete
        :return: None (204 No Content)
        """
        order = await order_dao.get_order_by_id(order_id=id, db_obj=db_obj)
        if not order:
            raise OrderNotFound(
                order_id=id, message=ErrorMessage.ORDER_NOT_FOUND.format(order_id=id)
            )
        await order_dao.delete_order(order, db_obj)

    @transaction
    async def cancel_order(self, order_id: UUID, db_obj: AsyncSession):
        order_db = await order_dao.get_order_by_id_with_details(
            order_id=order_id, db_obj=db_obj
        )
        if not order_db:
            raise OrderNotFound(
                order_id=order_id,
                message=ErrorMessage.ORDER_NOT_FOUND.format(order_id=order_id),
            )

        for history in order_db.order_histories:
            subproduct = history.subproducts
            product = subproduct.products
            qty = history.order_quantity

            subproduct.quantity += qty
            product.total_quantity += qty

        order_db.order_status = OrderStatus.CANCELLED
        order_db.updated_at = datetime.now()

        payment_db = order_db.payments
        if payment_db and payment_db.payment_status == PaymentStatus.SUCCESS:
            # Retrieve payment intent and charge
            intent = stripe.PaymentIntent.retrieve(
                payment_db.transaction_id, expand=["charges.data"]
            )
            charges = intent.get("charges", {}).get("data", [])
            if not charges:
                charge_id = intent.get("latest_charge")
            else:
                charge_id = charges[0]["id"]

            refund = stripe.Refund.create(charge=charge_id)

            # Update refund details
            payment_refund_update = PaymentRefundUpdate(
                payment_status=PaymentStatus.REFUND_INITIATED,
                refund_id=refund.id,
            )
            await payment_dao.update_refund_details(
                db_obj=db_obj,
                payment=payment_db,
                payment_refund_update=payment_refund_update,
            )

            # Update payment status after checking Stripe response
            if refund.status == StripeStatus.REFUND_SUCCESS_STATUS:
                payment_db.payment_status = PaymentStatus.REFUND_SUCCESS
                logger.info(f"Refund succeeded for payment {payment_db.id}")
            else:
                payment_db.payment_status = PaymentStatus.REFUND_FAILED
                logger.warning(
                    f"Refund status: {refund.status} for payment {payment_db.id}"
                )

        # update the product and subproducts
        updated_order = await order_dao.update_order_and_inventory_status(
            db_obj=db_obj,
            order=order_db,
            subproducts=[h.subproducts for h in order_db.order_histories],
            products=[h.subproducts.products for h in order_db.order_histories],
        )

        # Send cancellation email
        customer_id = remove_prefix(order_db.customer_id)
        customer = await customer_detail_dao.get_customer_detail(
            customer_id, db_obj=db_obj
        )
        customer_email = customer.email
        html_content = order_email_template(
            order=order_db, user=customer, cancelled_due_to_stock=False
        )

        logger.info(f"Starting to send cancellation email to {customer_email}")
        asyncio.create_task(
            send_order_email(email=customer_email, html_body=html_content)
        )
        logger.info(f"Email sent to {customer_email}")

        return Converter.order_db_to_dto(updated_order)

    async def get_all_orders(self, db_obj: AsyncSession, json: Json_pagination):
        """
        service layer function to fetch all orders.
        :param db_obj: The session object
        :param json: JSON payload for the pagination
        """
        total_count, orders = await order_dao.all_order(
            db_obj=db_obj,
            search=json.search,
            limit=json.limit,
            offset=json.offset,
        )
        converted_orders = [
            Converter.order_response_db_to_dto(order) for order in orders
        ]
        return UserOrderSummaryResponse(
            total_order_count=total_count, orders=converted_orders
        )


order_service = OrderService()
