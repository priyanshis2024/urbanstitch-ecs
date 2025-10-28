from uuid import UUID


class SubproductNotFound(Exception):
    """This class is for subproduct not found exception"""

    def __init__(self, subproduct_id: UUID, message: str):
        super().__init__()
        self.subproduct_id = subproduct_id
        self.message = message
