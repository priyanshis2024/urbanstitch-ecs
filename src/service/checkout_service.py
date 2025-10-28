import stripe
import json
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.service.checkout_converter import Converter
from src.dao.db import transaction
from src.exceptions.checkout import (
    CartNotFound,
    CarttProductAlreadyExists,
    CartDeletionUnauthorizedUser,
    EmptyCart,
)
from src.exceptions.user import UnauthorizedUser, UserIdMissing
from src.utils.user_id import ADMIN_USER_ID
from src.dto.checkout import (
    CartCreate,
    CartUpdate,
    CheckoutSessionRequest,
)
from src.dao.checkout import checkout_dao
from src.dao.models.product import Cart
from src.utils.utils import attach_prefix_to_uuid
from src.utils.constants import (
    UuidPrefix,
    PaymentMethod,
    StripeMode,
)
from src.dto.common import Jsonbody
from src.core.config import settings
from src.api.common_endpoints import PAYMENT_PROCESSING, CANCEL
from src.utils.constants import ErrorMessage
from typing import Optional
from src.middleware.logger import logger


stripe.api_key = settings.STRIPE_API_KEY


class CartService:
    async def get_cart_by_id(self, cart_id: UUID, db_obj: AsyncSession):
        """
        Service function to get a cart by ID asynchronously.
        :param db_obj: The session object
        :param cart_id: The ID of the cart to retrieve
        :return: cart object or None
        """
        result = await checkout_dao.get_cart_by_id(cart_id=cart_id, db_obj=db_obj)
        if not result:
            logger.error(f"Cart with id '{cart_id}' not found in the system.")
            raise CartNotFound(
                cart_id=cart_id,
                message=ErrorMessage.CART_NOT_FOUND.format(cart_id=cart_id),
            )
        return result

    @transaction
    async def create_cart_details(
        self, cart_create: CartCreate, user_id: UUID, db_obj: AsyncSession
    ):
        """
        Service function to create a new cart asynchronously.
        :param db_obj: The session object
        :param cart_create: The cart creation DTO
        :return: Created cart object (DTO)
        """

        if user_id == ADMIN_USER_ID:
            logger.error(
                f"Unauthorized user. User with id '{user_id}' is not authorized user to access this resource."
            )
            raise UnauthorizedUser(
                user_id=user_id,
                message=ErrorMessage.UNAUTHORIZED_USER.format(user_id=user_id),
            )

        current_user = attach_prefix_to_uuid(
            input_uuid=user_id, prefix=UuidPrefix.USER.value
        )
        existing_product = await checkout_dao.fetch_cart_product(
            db_obj=db_obj,
            subproduct_id=cart_create.subproduct_id,
            cart_id=Cart.id,
            user_id=current_user,
        )
        if existing_product:
            logger.error(
                f"Cart with subproduct id '{cart_create.subproduct_id}' already exists in the system."
            )
            raise CarttProductAlreadyExists(
                subproduct_id=cart_create.subproduct_id,
                message=ErrorMessage.CART_ALREADY_EXISTS.format(
                    subproduct_id=", ".join(cart_create.subproduct_id)
                ),
            )
        cart_db = Converter.cart_create_dto_to_db(cart_create)
        cart_db.user_id = current_user
        cart_db = await checkout_dao.create_cart(db_obj, cart_db)

        cart_details = await checkout_dao.fetch_cart_with_details(
            db_obj=db_obj, cart_id=cart_db.id
        )

        return Converter.cart_detail_dto_to_db(cart_details)

    @transaction
    async def update_existing_cart(
        self,
        cart_id: UUID,
        user_id: UUID,
        cart_update: CartUpdate,
        db_obj: AsyncSession,
    ):
        """
        Service function to update an existing cart asynchronously.
        :param db_obj: The session object
        :param cart_id: The ID of the cart to update
        :param cart_update: The cart update DTO
        :return: Updated cart object (DTO) or None
        """
        if user_id == ADMIN_USER_ID:
            logger.error(
                f"Unauthorized user. User with id '{user_id}' is not authorized user to access this resource."
            )
            raise UnauthorizedUser(
                user_id=user_id,
                message=ErrorMessage.UNAUTHORIZED_USER.format(user_id=user_id),
            )

        existing_cart_item = await checkout_dao.get_cart_by_id(
            db_obj=db_obj, cart_id=cart_id
        )

        if existing_cart_item:
            if cart_update.order_quantity:
                existing_cart_item.order_quantity = cart_update.order_quantity
            else:
                existing_cart_item.order_quantity += 1

            cart_db = await checkout_dao.update_cart(
                db_obj, existing_cart_item, cart_update
            )
            await checkout_dao.fetch_cart_with_details(
                db_obj=db_obj, cart_id=cart_db.id
            )
            return Converter.cart_detail_dto_to_db(existing_cart_item)

        cart_db = await checkout_dao.get_cart_by_id(cart_id=cart_id, db_obj=db_obj)
        if not cart_db:
            logger.error(f"Cart with id '{cart_id}' not found in the system.")
            raise CartNotFound(
                cart_id=cart_id,
                message=ErrorMessage.CART_NOT_FOUND.format(cart_id=cart_id),
            )

        update_cart = Converter.cart_update_dto_to_db(cart_update, cart_db)
        updated_cart = await checkout_dao.update_cart(db_obj, update_cart, cart_update)

        return Converter.cart_db_to_dto(updated_cart)

    @transaction
    async def delete_existing_cart(
        self, cart_id: Optional[UUID], user_id: Optional[str], db_obj: AsyncSession
    ):
        """
        Deletes a specific cart if both cart_id and user_id are present.
        Deletes all user carts if only user_id is present.
        Raises exception if only cart_id is provided.
        """
        user_id_str = attach_prefix_to_uuid(
            input_uuid=user_id, prefix=UuidPrefix.USER.value
        )
        if user_id == user_id_str:
            logger.error(
                f"Unauthorized user. User with id '{user_id}' is not authorized user to access this resource."
            )
            raise UnauthorizedUser(
                user_id=user_id,
                message=ErrorMessage.UNAUTHORIZED_USER.format(user_id=user_id),
            )

        else:
            if user_id and cart_id:
                cart_db = await checkout_dao.get_cart_by_id(
                    cart_id=cart_id, db_obj=db_obj
                )
                if not cart_db:
                    logger.error(f"Cart with id '{cart_id}' not found in the system.")
                    raise CartNotFound(
                        cart_id=cart_id,
                        message=ErrorMessage.CART_NOT_FOUND.format(cart_id=cart_id),
                    )
                if str(cart_db.user_id) != str(user_id_str):
                    logger.error(
                        f"User {user_id} is not authorized to delete cart {cart_id}"
                    )
                    raise CartDeletionUnauthorizedUser(
                        user_id=user_id,
                        cart_id=cart_id,
                        message=ErrorMessage.CART_DELETION_AUTHORIZATION.format(
                            user_id=user_id, cart_id=cart_id
                        ),
                    )
                await checkout_dao.delete_cart(db_obj, cart_db)

            elif user_id and not cart_id:
                user_carts = await checkout_dao.get_all_carts_by_user_id(
                    user_id=user_id, db_obj=db_obj
                )
                if not user_carts:
                    logger.error("Cart is already empty.")
                    raise EmptyCart(message=ErrorMessage.CART_EMPTY.format())
                for cart in user_carts:
                    await checkout_dao.delete_cart(db_obj, cart)

            elif cart_id and not user_id:
                logger.error("User id is missing.")
                raise UserIdMissing(message=ErrorMessage.USER_ID_MISSING.format())

        return {"status": "Success"}

    async def get_all_cart(self, json: Jsonbody, db_obj: AsyncSession, user_id: str):
        """
        Service function to get all cart asynchronously.
        :param db_obj: The session object
        :return: List of cart DTO
        """
        response = await checkout_dao.all_cart(
            db_obj=db_obj,
            user_id=user_id,
            search=json.search,
            sort_by=json.sort_by,
            sort_order=json.sort_order,
            limit=json.limit,
            offset=json.offset,
        )

        return Converter.cart_detail_list_response_db_to_dto(response)

    async def get_all_cart(self, json: Jsonbody, db_obj: AsyncSession, user_id: str):
        """
        Service function to get all cart asynchronously.
        :param db_obj: The session object
        :return: List of cart DTO
        """
        response = await checkout_dao.all_cart(
            db_obj=db_obj,
            user_id=user_id,
            search=json.search,
            sort_by=json.sort_by,
            sort_order=json.sort_order,
            limit=json.limit,
            offset=json.offset,
        )

        return Converter.cart_detail_list_response_db_to_dto(response)

    async def create_checkout_session(self, request: CheckoutSessionRequest) -> dict:
        products = request.products
        payment_id = request.payment_id
        order_id = request.order_id
        line_items = Converter.convert_to_line_items(products)

        session = stripe.checkout.Session.create(
            payment_method_types=[PaymentMethod.CARD.name.lower()],
            line_items=line_items,
            mode=StripeMode.PAYMENT,
            success_url=f"http://{settings.URL_HOST}:{settings.URL_PORT}/{PAYMENT_PROCESSING}?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"http://{settings.URL_HOST}:{settings.URL_PORT}/{CANCEL}",
            metadata={"order_id": order_id, "payment_id": payment_id},
        )
        return Converter.checkout_response_db_to_dto(session, line_items)


cart_service = CartService()
