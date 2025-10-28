## TODO: This file is used to handle the OAuth2 authentication process. It contains the TokenBearer class and its subclasses for access and refresh tokens.
# This function is used to protect the routes with access and refresh tokens.

from fastapi import Request
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from src.utils.utils import verify_token
from src.exceptions.user_authentication import (
    MissingAccessToken,
    MissingRefreshToken,
)
from src.utils.constants import ErrorMessage, Message
from src.middleware.logger import logger


class TokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):
        logger.debug("Initializing TokenBearer class _init__ method")
        super().__init__(auto_error=auto_error)

    def verify_token_data(self):  # A parent class method to verify token data
        """
        This method should be overridden in subclasses to implement specific token data verification logic.
        """
        logger.debug(
            "Verify token data in TokenBearer's verify_token_data first method"
        )

        raise NotImplementedError(Message.OVERRIDE_SUBCLASS)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        logger.debug("Credentials in TokenBearer ===", creds)
        token = creds.credentials  # Extracting the token from the credentials
        logger.debug("Token in TokenBearer ===", token)
        token_data = verify_token(token)
        logger.debug("Token data in TokenBearer ===", token_data)
        # Verifying the token using the verify_token function
        a = self.verify_token_data(token_data)
        logger.debug("Verified token data in TokenBearer __call__ method ===", a)
        # calling verify_token_data function for the token type verification if it is access token or refresh token? (If we does not provide this then for it takes both access and refresh token as valid token)
        # # If it is refresh token, then we are raising the exception such as please provide access token
        # # If it is access token, then we are not raising any exception if access token is not expired.

        return token_data


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        logger.debug(
            "Verify token data in AccessTokenBearer's verify_token_data method"
        )
        if token_data and token_data.get("refresh"):
            logger.error("Access token is missing")
            raise MissingAccessToken(message=ErrorMessage.ACCESS_TOKEN_MISSING.format())


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        logger.debug(
            "Verify token data in RefreshTokenBearer's verify_token_data method"
        )
        if token_data and not token_data.get("refresh"):
            logger.error("Refresh token is missing")
            raise MissingRefreshToken(
                message=ErrorMessage.REFRESH_TOKEN_MISSING.format()
            )
