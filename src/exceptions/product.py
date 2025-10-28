from uuid import UUID


class ProductNotFound(Exception):
    """This class is for product not found exception"""

    def __init__(self, product_id: UUID, message: str):
        super().__init__()
        self.product_id = product_id
        self.message = message
