from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
import stripe
from uuid import UUID
from src.service.payment_converter import Converter
from src.dao.db import transaction
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.payment import payment_dao
from src.dao.order import order_dao
from src.dao.customer_details import customer_detail_dao
from src.dto.payment import (
    PaymentCreate,
    PaymentStatusUpdate,
    PaymentRefundUpdate,
)
from src.exceptions.payment import PaymentNotFound
from src.exceptions.user import UnauthorizedUser
from src.exceptions.order import OrderNotFound
from src.utils.constants import ErrorMessage, OrderStatus, PaymentStatus, StripeStatus
from src.utils.user_id import ADMIN_USER_ID
from src.middleware.logger import logger
from datetime import datetime
from src.utils.utils import remove_prefix
from src.utils.email_sender import send_order_email
from src.utils.order_template import order_email_template


class PaymentService:

    async def get_payment_by_id(self, payment_id: UUID, db_obj: AsyncSession):
        """Service function to get payment details by id."""
        result = await payment_dao.get_payment_by_id(
            payment_id=payment_id, db_obj=db_obj
        )
        if not result:
            logger.error(f"Payment with id '{payment_id}' not found in the system.")
            raise PaymentNotFound(
                payment_id=payment_id,
                message=ErrorMessage.PAYMENT_NOT_FOUND.format(payment_id=payment_id),
            )
        return result

    @transaction
    async def create_payment(self, payment_create: PaymentCreate, db_obj: AsyncSession):
        """
        Service function to creates a payment for an order.
        """
        payment_db = Converter.payment_create_dto_to_db(payment_create)
        payment = await payment_dao.create_payment(payment_db, db_obj)
        return Converter.payment_db_to_dto(payment)

    async def get_all_payment(self, db_obj: AsyncSession):
        """Service function to get all payment details"""
        payments = await payment_dao.all_payment(db_obj)
        return [Converter.payment_db_to_dto(payment) for payment in payments]

    @transaction
    async def delete_payment(
        self, payment_id: UUID, user_id: str, db_obj: AsyncSession
    ):
        """Service function to delete a payment details"""
        if user_id != ADMIN_USER_ID:
            logger.error(
                f"Unauthorized user. User with id '{user_id}' is not authorized user to access this resource."
            )
            raise UnauthorizedUser(
                user_id=user_id,
                message=ErrorMessage.UNAUTHORIZED_USER.format(user_id=user_id),
            )
        payment_db = await payment_dao.get_payment_by_id(payment_id, db_obj)
        if not payment_db:
            logger.error(f"Payment with id '{payment_id}' not found in the system.")
            raise PaymentNotFound(
                payment_id=payment_id,
                message=ErrorMessage.PAYMENT_NOT_FOUND.format(payment_id=payment_id),
            )
        if payment_db:
            await payment_dao.delete_payment(payment_db, db_obj)

    @transaction
    async def update_payment_details(
        self,
        db_obj: AsyncSession,
        payment_id: UUID,
        payment_update_status: PaymentStatusUpdate,
    ):
        """
        Service function to update payment status and transaction id.
        Based on the payment status, it updates the order status.
        Based on the order status, it updates the inventory status and send the email in the asynchronous way.
        :param db_obj: The session object
        :param payment_id: The ID of the payment to update
        :param payment_update_status: The payment update status DTO
        """
        payment_db = await payment_dao.get_payment_by_id(payment_id, db_obj)
        if not payment_db:
            raise PaymentNotFound(
                payment_id=payment_id,
                message=ErrorMessage.PAYMENT_NOT_FOUND.format(payment_id=payment_id),
            )

        await payment_dao.update_status_and_transaction_id(
            db_obj=db_obj,
            payment=payment_db,
            payment_update_status=payment_update_status,
        )

        # fetch order details for the payment
        order_db = await order_dao.get_order_by_id_with_details(
            order_id=payment_db.order_id, db_obj=db_obj
        )

        if not order_db:
            raise OrderNotFound(
                order_id=payment_db.order_id,
                message=ErrorMessage.ORDER_NOT_FOUND.format(
                    order_id=payment_db.order_id
                ),
            )

        # Check payment status and update order status accordingly
        if payment_update_status.payment_status == PaymentStatus.SUCCESS:
            # check the stock availability
            insufficient_stock = False
            subproducts_to_update = []
            products_to_update = []

            for history in order_db.order_histories:
                subproduct = history.subproducts
                product = subproduct.products
                qty = history.order_quantity

                if subproduct.quantity < qty:
                    insufficient_stock = True
                    break

            # If stock is insufficient, cancel the order
            if insufficient_stock:
                order_db.order_status = OrderStatus.CANCELLED
                order_db.updated_at = datetime.now()
                logger.info(
                    f"Order cancelled due to insufficient stock for order_id: {order_db.id}"
                )
                intent = stripe.PaymentIntent.retrieve(
                    payment_db.transaction_id, expand=["charges.data"]
                )
                charges = intent.get("charges", {}).get("data", [])
                if not charges:
                    charge_id = intent.get("latest_charge")
                else:
                    charge_id = charges[0]["id"]
                refund = stripe.Refund.create(charge=charge_id)
                payment_refund_update = PaymentRefundUpdate(
                    payment_status=PaymentStatus.REFUND_INITIATED, refund_id=refund.id
                )
                await payment_dao.update_refund_details(
                    db_obj=db_obj,
                    payment=payment_db,
                    payment_refund_update=payment_refund_update,
                )
                if refund.status == StripeStatus.REFUND_SUCCESS_STATUS:
                    payment_db.payment_status = PaymentStatus.REFUND_SUCCESS
                    logger.info(f"Refund succeeded for payment {payment_id}")
                else:
                    payment_db.payment_status = PaymentStatus.REFUND_FAILED
                    logger.warning(
                        f"Refund status: {refund.status} for payment {payment_id}"
                    )

            # If stock is sufficient, confirm the order and update quantities
            else:
                for history in order_db.order_histories:
                    subproduct = history.subproducts
                    product = subproduct.products
                    qty = history.order_quantity

                    subproduct.quantity -= qty
                    product.total_quantity -= qty
                    subproducts_to_update.append(subproduct)
                    products_to_update.append(product)

                order_db.order_status = OrderStatus.CONFIRMED
                order_db.updated_at = datetime.now()
                logger.info(
                    f"Order confirmed and order status is updated for order_id {order_db.id}"
                )

                await order_dao.update_order_and_inventory_status(
                    db_obj=db_obj,
                    order=order_db,
                    subproducts=subproducts_to_update,
                    products=products_to_update,
                )
                logger.info(
                    f"Order confirmed and inventory updated in the product and subproduct for order_id {order_db.id}"
                )

            customer_id = remove_prefix(order_db.customer_id)
            customer = await customer_detail_dao.get_customer_detail(
                customer_id, db_obj=db_obj
            )
            customer_email = customer.email
            html_content = order_email_template(
                order=order_db, user=customer, cancelled_due_to_stock=True
            )
            logger.info(f"Starting to send email to {customer_email}")
            asyncio.create_task(
                send_order_email(email=customer_email, html_body=html_content)
            )
            logger.info(f"Email sent to {customer_email}")

        elif payment_update_status.payment_status == PaymentStatus.FAILED:
            return

        return Converter.payment_db_to_dto(payment_db)


payment_service = PaymentService()
