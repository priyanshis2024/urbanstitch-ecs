from src.dto.checkout import (
    CartCreate,
    CartDetailResponse,
    CartUpdate,
    CartResponse,
    CartListDetailResponse,
    ProductDTO,
    CheckoutSessionResponse,
)
from src.dao.models.product import Cart
from fastapi.encoders import jsonable_encoder
import uuid
from src.utils.constants import Currency, ProductTax


class Converter:
    def cart_create_dto_to_db(cart_create: CartCreate):
        """
        Convert a CartCreate DTO to a cart database model.
        :param cart_create: CartCreate DTO
        :return: cart database model
        """
        return Cart(
            subproduct_id=cart_create.subproduct_id,
            order_quantity=cart_create.order_quantity,
        )

    def cart_detail_dto_to_db(cart: Cart):
        """
        Convert a cart  to CartDetailResponse DTO to DB.
        """
        subproduct = cart.subproducts
        product = subproduct.products
        size = subproduct.sizes

        return CartDetailResponse(
            id=cart.id,
            subproduct_id=subproduct.id,
            name=product.name,
            description=product.description,
            size=size.size,
            color=subproduct.color,
            order_quantity=cart.order_quantity,
            price=subproduct.price,
            images=(
                subproduct.images.split(",")
                if isinstance(subproduct.images, str)
                else subproduct.images
            ),
        )

    def cart_db_to_dto(cart: CartResponse):
        """
        Convert a cart database model to a CartResponse DTO.
        :param cart: cart database model
        :return: CartResponse DTO
        """
        cart_dict = jsonable_encoder(cart)
        return CartResponse(**cart_dict)

    def cart_update_dto_to_db(cart_update: CartUpdate, cart: Cart):
        """
        Convert a CartUpdate DTO to a cart database model (updating an existing cart).
        :param cart_update: Existing cart database model
        :return: Updated cart database model
        """
        for key, value in cart_update.model_dump(exclude_unset=True).items():
            setattr(cart, key, value)
        return cart

    def cart_detail_list_response_db_to_dto(cart_data):
        """
        Convert cart query response to DTO.
        """
        return CartListDetailResponse(
            total_cart_product_count=cart_data["total_cart_product_count"],
            cart_products=[
                Converter.cart_detail_dto_to_db(cart)
                for cart in cart_data["cart_products"]
            ],
        )

    def convert_to_line_items(products: list[ProductDTO]) -> list:
        return [
            {
                "price_data": {
                    "currency": Currency.INR,
                    "product_data": {
                        "name": f"{product.name} - {product.color} - {product.size}",
                    },
                    "unit_amount": int(product.price * ProductTax.PAISA),
                },
                "quantity": product.quantity,
            }
            for product in products
        ]

    def checkout_response_db_to_dto(
        session, line_items: list
    ) -> CheckoutSessionResponse:
        return CheckoutSessionResponse(
            id=session.id,
            object=session.object,
            url=session.url,
            payment_status=session.payment_status,
            payment_method_types=session.payment_method_types,
            shipping_cost=session.shipping_cost,
            amount_total=session.amount_total,
            amount_subtotal=session.amount_subtotal,
            customer=session.customer,
            customer_email=session.customer_email,
            customer_details=session.customer_details,
            payment_link=session.payment_link,
            status=session.status,
            session=session.object,
            line_items=line_items,
        )
