from fastapi import HTTPException, status


class UserNotFound(Exception):
    """This class is for user not found exception"""

    def __init__(self, user_id: str, message: str):
        super().__init__()
        self.user_id = user_id
        self.message = message


class InvalidSortingAttribute(HTTPException):
    """
    Exception raised when the provided attribute for sorting is invalid.
    """

    def __init__(self, attribute: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid attribute '{attribute}' for sorting",
        )


class UnauthorizedUser(Exception):
    """
    Exception raised when the provided user is unauthorized.
    """

    def __init__(self, user_id: str, message: str):
        super().__init__()
        self.user_id = user_id
        self.message = message


class UserIdMissing(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.message = message


class UserEmailNotFound(Exception):
    """This class is for user not found exception"""

    def __init__(self, email: str, message: str):
        super().__init__()
        self.email = email
        self.message = message
