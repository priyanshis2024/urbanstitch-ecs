from uuid import UUID


class PaymentNotFound(Exception):
    """This class is for payment details not found exception"""

    def __init__(self, payment_id: UUID, message: str):
        super().__init__()
        self.payment_id = payment_id
        self.message = message
