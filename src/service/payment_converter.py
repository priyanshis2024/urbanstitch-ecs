from src.dao.models.product import Payment
from src.dto.payment import (
    PaymentCreate,
    PaymentResponse,
)
from fastapi.encoders import jsonable_encoder


class Converter:
    def payment_create_dto_to_db(payment_create: PaymentCreate):
        return Payment(
            order_id=payment_create.order_id,
            amount=payment_create.amount,
            payment_status=payment_create.payment_status,
            payment_method=payment_create.payment_method,
            transaction_id=payment_create.transaction_id,
        )

    def payment_db_to_dto(payment_response: PaymentResponse):
        """
        Convert a payment database model to a Order.
        :param payment: Payment database model
        :return: Payment model
        """
        payment_dict = jsonable_encoder(payment_response)
        return PaymentResponse(**payment_dict)
