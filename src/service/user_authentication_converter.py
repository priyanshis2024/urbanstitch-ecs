from src.dao.models.user import UserAuthentications
from src.dto.user_authenticate import UserAuthenticationCreate


class Converter:
    def user_authentication_create_dto_to_db(
        auth_data: UserAuthenticationCreate,
    ) -> UserAuthentications:
        """
        Convert DTO to UserAuthentications model for database insertion.
        """
        return UserAuthentications(
            user_id=auth_data.user_id,
            access_token=auth_data.access_token,
            refresh_token=auth_data.refresh_token,
            expired_at=auth_data.expired_at,
        )
