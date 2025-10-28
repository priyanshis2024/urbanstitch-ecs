from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from src.dao.models.product import Payment
from src.dto.payment import PaymentCreate, PaymentStatusUpdate, PaymentRefundUpdate


class payment_dao:
    async def get_payment_by_id(payment_id: UUID, db_obj: AsyncSession):
        result = await db_obj.execute(select(Payment).filter(Payment.id == payment_id))
        return result.scalars().first()

    async def create_payment(payment: PaymentCreate, db_obj: AsyncSession):
        db_obj.add(payment)
        await db_obj.commit()
        await db_obj.refresh(payment)
        return payment

    async def delete_payment(payment: Payment, db_obj: AsyncSession):
        await db_obj.delete(payment)

    async def all_payment(db_obj: AsyncSession):
        query = select(Payment)
        result = await db_obj.execute(query)
        return result.scalars().all()

    async def update_status_and_transaction_id(
        db_obj: AsyncSession,
        payment: Payment,
        payment_update_status: PaymentStatusUpdate,
    ):
        """
        The update_status_and_transaction_id function is used to update the status of payment and add the transaction ID for the given payment id.

        :param payment: Get the payment details
        :param new_status: Updated new payment status
        :param db_obj: database object
        """
        for key, value in payment_update_status.dict(exclude_unset=True).items():
            setattr(payment, key, value)
        return payment

    async def update_refund_details(
        db_obj: AsyncSession,
        payment: Payment,
        payment_refund_update: PaymentRefundUpdate,
    ):
        """
        The update_refund_details function is used to update the status of payment and add the transaction ID for the given payment id.

        :param payment: Get the payment details
        :param payment_refund_update: Updated payment's refund details
        :param db_obj: database object
        """
        for key, value in payment_refund_update.dict(exclude_unset=True).items():
            setattr(payment, key, value)
        return payment
