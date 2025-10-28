from sqlalchemy.ext.asyncio import AsyncSession
from src.dto.user_authenticate import UserAuthenticationCreate
from datetime import datetime, timedelta
from sqlalchemy import select
from src.dao.models.user import User


class user_authenticate_dao:
    async def create_user_authentication(
        db_obj: AsyncSession, auth_data: UserAuthenticationCreate
    ):
        """This function is for creating user authentication details for the access token and refresh token."""
        db_obj.add(auth_data)
        await db_obj.commit()
        await db_obj.refresh(auth_data)
        return auth_data

    async def save_otp(email: str, otp: str, db_obj: AsyncSession):
        result = await db_obj.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if user:
            user.otp = otp
            db_obj.add(user)
            await db_obj.commit()

    async def get_valid_otp(email: str, db_obj: AsyncSession):
        result = await db_obj.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if user and user.otp and user.updated_at:
            if user.updated_at + timedelta(minutes=10) > datetime.now():
                return user.otp
        return None
