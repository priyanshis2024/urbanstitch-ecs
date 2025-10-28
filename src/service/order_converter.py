from src.dao.models.product import Order, OrderHistory
from src.dto.order import (
    OrderCreate,
    OrderResponse,
    OrderHistoryCreate,
    OrderHistoryResponse,
    UserOrderResponse,
    UserOrderCreationResponse,
    OrderHistoryListResponse,
    OrderStatusUpdate,
    OrderSummaryResponse,
)
from src.dto.customer_details import CustomerDetailResponse
from src.dto.payment import PaymentResponse
from fastapi.encoders import jsonable_encoder


class Converter:
    def order_db_to_dto(order_response: OrderResponse):
        """
        Convert a order database model to a Order DTO.
        :param order: Order database model
        :return: Order model
        """
        order_dict = jsonable_encoder(order_response)
        return OrderResponse(**order_dict)

    def order_response_db_to_dto(order: Order) -> UserOrderResponse:
        """
        Convert Order DB object to UserOrderResponse DTO.
        """
        return UserOrderResponse(
            order=OrderResponse(
                id=order.id,
                user_id=str(order.user_id),
                customer_id=str(order.customer_id),
                order_status=order.order_status,
                created_at=order.created_at,
                updated_at=order.updated_at,
            ),
            order_products=OrderHistoryListResponse(
                total_product_count=len(order.order_histories),
                products=[
                    OrderHistoryResponse(
                        id=op.id,
                        order_id=op.order_id,
                        subproduct_id=op.subproduct_id,
                        price=op.price,
                        order_quantity=op.order_quantity,
                        created_at=op.created_at,
                        updated_at=op.updated_at,
                    )
                    for op in order.order_histories
                ],
            ),
        )

    def user_order_creation_dto_to_db(order: Order) -> UserOrderCreationResponse:
        """
        Convert Order DB object to UserOrderCreationResponse DTO.
        """
        order_response = Converter.order_response_db_to_dto(order)

        return UserOrderCreationResponse(
            order=order_response.order,
            order_products=order_response.order_products,
            total_order_amount=float(
                sum(op.price * op.order_quantity for op in order.order_histories)
            ),
        )

    def order_summary_db_to_dto(order: Order) -> OrderSummaryResponse:
        user_id = str(order.user_id.split(":")[1])
        customer = order.customer_details
        payment = order.payments
        return OrderSummaryResponse(
            customer_details=CustomerDetailResponse(
                id=customer.id,
                user_id=user_id,
                address_type=customer.address_type,
                address=customer.address,
                landmark=customer.landmark,
                city=customer.city,
                state=customer.state,
                country=customer.country,
                pincode=customer.pincode,
                contact=customer.contact,
                email=customer.email,
                first_name=customer.first_name,
                last_name=customer.last_name,
                created_at=customer.created_at,
                updated_at=customer.updated_at,
            ),
            payment_details=PaymentResponse(
                id=payment.id,
                order_id=payment.order_id,
                amount=payment.amount,
                payment_status=payment.payment_status,
                payment_method=payment.payment_method,
                transaction_id=payment.transaction_id,
                payment_at=payment.payment_at,
            ),
            order=Converter.user_order_creation_dto_to_db(order).order,
            order_products=Converter.user_order_creation_dto_to_db(
                order
            ).order_products,
            total_order_amount=Converter.user_order_creation_dto_to_db(
                order
            ).total_order_amount,
        )

    def order_history_create_dto_to_db(order_history_create: OrderHistoryCreate):
        return OrderHistory(
            order_id=order_history_create.order_id,
            subproduct_id=order_history_create.subproduct_id,
            price=order_history_create.price,
            order_quantity=order_history_create.order_quantity,
        )

    def order_history_db_to_dto(order_history: OrderHistory) -> OrderHistoryResponse:
        order_history_dict = order_history.__dict__
        return OrderHistoryResponse(
            id=order_history_dict["id"],
            order_id=order_history_dict["order_id"],
            subproduct_id=order_history_dict["subproduct_id"],
            price=order_history_dict["price"],
            order_quantity=order_history_dict["order_quantity"],
            created_at=order_history_dict["created_at"],
            updated_at=order_history_dict["updated_at"],
        )

    def order_status_update_dto_to_db(
        order_status_update: OrderStatusUpdate, order: Order
    ):
        for key, value in order_status_update.model_dump(exclude_unset=True).items():
            setattr(order, key, value)
        return order
