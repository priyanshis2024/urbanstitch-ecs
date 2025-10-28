"""This module include external settings or configurations,
for example secret keys, database credentials"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """class for reading configurations from env file"""

    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    STRIPE_API_KEY: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    URL_HOST: str
    URL_PORT: int
    SENDER_EMAIL: str
    SMTP_PORT: int
    SMTP_SERVER: str
    SMTP_PASSWORD: str
    BACKEND_KEY: str

    class Config:
        """
        settings for Settings configurations
        this class is to setup environment variables locally
        """

        env_file = ".env"
        extra = "allow"


settings = Settings()
