from uuid import UUID


class OrderNotFound(Exception):
    """This class is for order details not found exception"""

    def __init__(self, order_id: UUID, message: str):
        super().__init__()
        self.order_id = order_id
        self.message = message


class UserOrderNotFound(Exception):
    """This class is for order details not found for the user."""

    def __init__(self, user_id: UUID, message: str):
        super().__init__()
        self.user_id = user_id
        self.message = message
