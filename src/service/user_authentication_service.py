from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.email_sender import send_otp_email
from src.dao.user_authenticate import user_authenticate_dao
from src.dao.users import user_dao
from src.dao.db import transaction
from src.dto.user_authenticate import (
    OTPGenerationRequest,
    OTPGenerateResponse,
    UserAuthenticationCreate,
    UserLogin,
)
from src.exceptions.user_authentication import OTPExpired, InvalidOTP
from src.exceptions.user import UserEmailNotFound
from datetime import timedelta, datetime
from src.service.user_authentication_converter import Converter
from src.middleware.logger import logger
from src.utils.utils import (
    generate_password_hash,
    decrypt_password,
    create_access_token,
    generate_OTP,
)
from src.core.config import settings
from src.utils.constants import Message, ErrorMessage, Status
from src.exceptions.user_authentication import InvalidPassword


class UserAuthenticationService:
    @transaction
    async def generate_otp_service(
        self, otp_request: OTPGenerationRequest, db_obj: AsyncSession
    ):
        otp = generate_OTP()
        await user_authenticate_dao.save_otp(
            email=otp_request.email, otp=otp, db_obj=db_obj
        )
        await send_otp_email(email=otp_request.email, otp=otp)
        return OTPGenerateResponse(message=Message.OTP_SUCCESS_MESSAGE)

    @transaction
    async def verify_otp_service(self, email: str, otp: str, db_obj: AsyncSession):
        saved_otp = await user_authenticate_dao.get_valid_otp(
            email=email, db_obj=db_obj
        )
        if saved_otp is None:
            raise OTPExpired(message=Message.OTP_EXPIRED.format())
        if saved_otp != otp:
            raise InvalidOTP(message=Message.INVALID_OTP.format())
        if saved_otp == otp:
            user_db = await user_dao.fetch_email_detail(db_obj=db_obj, email=email)
            user_db.status = Status.ENABLED
            await user_dao.update_status(db_obj, user_db, user_db.status)
            return {"message": Message.OTP_VERIFICATION_MESSAGE}

    async def get_user_by_email(self, email: str, db_obj: AsyncSession):
        """
        Service function to get a user by email asynchronously.
        :param db_obj: The session object
        :return: User object or None
        """
        result = await user_dao.fetch_email_detail(email=email, db_obj=db_obj)
        if not result:
            logger.error(f"User info with email '{email}' not found in the system.")
            raise UserEmailNotFound(
                email=email,
                message=ErrorMessage.USER_EMAIL_NOT_FOUND.format(email=email),
            )
        return result

    @transaction
    async def login_user_service(
        self, user_login_data: UserLogin, db_obj: AsyncSession
    ) -> dict:
        """
        Service function to handle user login, token creation, and user authentication creation logic.
        """
        email = user_login_data.email
        password = user_login_data.password
        encrypted_aes_key = user_login_data.encrypted_aes_key
        encrypted_aes_iv = user_login_data.encrypted_aes_iv

        user = await user_dao.fetch_email_detail(email=email, db_obj=db_obj)

        if user is not None:
            decrypted_password = decrypt_password(
                encrypted_password=password,
                encrypted_aes_key=encrypted_aes_key,
                iv=encrypted_aes_iv,
            )

            hashed_password = generate_password_hash(decrypted_password)

            if hashed_password == user.password:
                access_token = create_access_token(
                    user_data={"email": user.email, "user_id": str(user.id)},
                    expiry=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
                )

                refresh_token = create_access_token(
                    user_data={"email": user.email, "user_id": str(user.id)},
                    refresh=True,
                    expiry=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
                )

                auth_data = UserAuthenticationCreate(
                    user_id=str(user.id),
                    access_token=access_token,
                    refresh_token=refresh_token,
                    expired_at=datetime.now()
                    + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
                )

                user_authentication_db = Converter.user_authentication_create_dto_to_db(
                    auth_data
                )
                await user_authenticate_dao.create_user_authentication(
                    db_obj=db_obj, auth_data=user_authentication_db
                )
                return {
                    "message": Message.LOGIN_SUCCESS,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "id": str(user.id)},
                }
        raise InvalidPassword(message=ErrorMessage.INVALID_PASSWORD.format())


user_authentication_service = UserAuthenticationService()
