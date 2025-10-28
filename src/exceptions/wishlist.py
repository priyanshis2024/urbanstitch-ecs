from fastapi import status
from uuid import UUID


class WishlistProductAlreadyExists(Exception):
    """This class is for wishlist product already exists exception"""

    def __init__(self, wishlist_id: UUID, message: str):
        super().__init__()
        self.wishlist_id = wishlist_id
        self.message = message


class WishlistNotFound(Exception):
    """This class is for wishlist details not found exception"""

    def __init__(self, wishlist_id: UUID, message: str):
        super().__init__()
        self.wishlist_id = wishlist_id
        self.message = message
