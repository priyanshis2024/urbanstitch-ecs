"""This module contains the Address module exceptions."""

from uuid import UUID


class CustomerDetailNotFound(Exception):
    """This class is for address not found exception"""

    def __init__(self, customer_detail_id: UUID, message: str):
        super().__init__()
        self.customer_detail_id = customer_detail_id
        self.message = message
