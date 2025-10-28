from fastapi import HTTPException, APIRouter, Depends
from src.dao.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.dto.user_authenticate import OTPGenerationRequest, UserLogin
from src.service.user_authentication_service import user_authentication_service
from fastapi.responses import JSONResponse
from src.utils.oauth2 import RefreshTokenBearer
from datetime import datetime
from src.exceptions.user_authentication import InvalidOrExpiredToken
from src.utils.constants import ErrorMessage
from src.utils.utils import create_access_token

router = APIRouter(tags=["User Authentication module"])


@router.patch("/otp-generation")
async def otp_generation_and_mail_response(
    otp_request: OTPGenerationRequest, db_obj: AsyncSession = Depends(get_db)
):
    return await user_authentication_service.generate_otp_service(
        otp_request=otp_request, db_obj=db_obj
    )


@router.patch("/otp-verification")
async def otp_verification(
    email: str,
    otp: str,
    db_obj: AsyncSession = Depends(get_db),
):
    return await user_authentication_service.verify_otp_service(
        email=email, otp=otp, db_obj=db_obj
    )


@router.post("/login")
async def login_users(
    user_login_data: UserLogin, db_obj: AsyncSession = Depends(get_db)
):
    """
    API endpoint to log in a user by verifying their email and password.
    """
    try:
        response_data = await user_authentication_service.login_user_service(
            user_login_data=user_login_data, db_obj=db_obj
        )
        return JSONResponse(content=response_data)

    except HTTPException as e:
        raise e


@router.get("/refresh-token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    """
    API endpoint for the creation of a new access token using a refresh token.
    """
    expiry_timestamp = token_details["exp"]
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])
        return JSONResponse(content={"access_token": new_access_token})
    raise InvalidOrExpiredToken(message=ErrorMessage.INVALID_OR_EXPIRED_TOKEN.format())
