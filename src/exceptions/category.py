from uuid import UUID


class CategoryNotFound(Exception):
    """This class is for category not found exception"""

    def __init__(self, category_id: UUID, message: str):
        super().__init__()
        self.category_id = category_id
        self.message = message


class CategoryAlreadyExists(Exception):
    """This class is for category already exists exception"""

    def __init__(self, category_id: UUID, message: str):
        super().__init__()
        self.category_id = category_id
        self.message = message
