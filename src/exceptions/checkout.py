from uuid import UUID


class CartNotFound(Exception):
    """This class is for cart details not found exception"""

    def __init__(self, cart_id: UUID, message: str):
        super().__init__()
        self.cart_id = cart_id
        self.message = message


class EmptyCartError(Exception):
    """This class is for cart details not found because cart is empty exception for order creation."""

    def __init__(self, message: str):
        super().__init__()
        self.message = message


class CarttProductAlreadyExists(Exception):
    """This class is for cart product already exists exception"""

    def __init__(self, subproduct_id: UUID, message: str):
        super().__init__()
        self.subproduct_id = subproduct_id
        self.message = message


class CartDeletionUnauthorizedUser(Exception):
    """This class is for to check ownership of the user with the cart hence no other user can delete the cart details."""

    def __init__(self, user_id: str, cart_id: UUID, message: str):
        super().__init__()
        self.user_id = user_id
        self.cart_id = cart_id
        self.message = message


class EmptyCart(Exception):
    """This class is for cart details not found because cart is empty exception"""

    def __init__(self, message: str):
        super().__init__()
        self.message = message
