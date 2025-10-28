"""This module contains the user role module exceptions."""


class UserRoleNotFound(Exception):
    """This class is for user not found exception"""

    def __init__(self, user_role_id: int, message: str):
        super().__init__()
        self.user_role_id = user_role_id
        self.message = message


class InvalidUserRole(Exception):
    """This class raise exception when an invalid user role is found"""

    def __init__(self, user_role_id: int, message: str):
        super().__init__()
        self.user_role_id = user_role_id
        self.message = message


class UserRoleExist(Exception):
    """This class raise exception when trying to assign a user role that already exists."""

    def __init__(self, user_role_id: int, message: str):
        super().__init__()
        self.user_role_id = user_role_id
        self.message = message
