from uuid import UUID


class SubcategoryNotFound(Exception):
    """This class is for subcategory not found exception"""

    def __init__(self, subcategory_id: UUID, message: str):
        super().__init__()
        self.subcategory_id = subcategory_id
        self.message = message
