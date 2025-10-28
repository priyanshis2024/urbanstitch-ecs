from uuid import UUID

""" This module contains custom exceptions for the contact us feature."""


class ContactUsNotFound(Exception):
    """This class is for contact us details not found exception"""

    def __init__(self, contact_us_id: UUID, message: str):
        super().__init__()
        self.contact_us_id = contact_us_id
        self.message = message
