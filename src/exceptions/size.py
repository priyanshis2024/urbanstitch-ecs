from uuid import UUID

"""This module contains the Size module custom exceptions."""


class SizeNotFound(Exception):
    """This class is for size not found exception"""

    def __init__(self, size_id: UUID, message: str):
        super().__init__()
        self.size_id = size_id
        self.message = message


class SizeAlreadyExists(Exception):
    """This class is for size already exists exception"""

    def __init__(self, size_id: UUID, message: str):
        super().__init__()
        self.size_id = size_id
        self.message = message
