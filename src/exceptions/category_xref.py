from uuid import UUID


class CategoryXrefSubcategoryNotFound(Exception):
    """This class is for subcategory not found for their category exception"""

    def __init__(self, category_id: UUID, message: str):
        super().__init__()
        self.category_id = category_id
        self.message = message
