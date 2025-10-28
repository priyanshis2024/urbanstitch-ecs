from uuid import UUID


class ReviewNotFound(Exception):
    """This class is for review not found exception"""

    def __init__(self, review_id: UUID, message: str):
        super().__init__()
        self.review_id = review_id
        self.message = message
