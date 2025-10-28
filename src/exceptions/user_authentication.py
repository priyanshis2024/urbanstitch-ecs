"""This module is for raising the user authentication exceptions."""


class InvalidPassword(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.message = message


class InvalidOrExpiredToken(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.message = message


class MissingAccessToken(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.message = message


class MissingRefreshToken(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.message = message


class ExpiredToken(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.message = message


class OTPExpired(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.message = message


class InvalidOTP(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.message = message


class FailedMail(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.message = message
