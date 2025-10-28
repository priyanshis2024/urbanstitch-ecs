from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.core.config import settings
import asyncio

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_db():
    """
    This function creates a new database async session.
    """
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


def transaction(func):
    """
    This function is a decorator that wraps the function it's applied to.
    It attempts to commit changes, and if there are any errors, it rolls back those changes.
    This helps avoid leaving behind partially-committed transactions when things go wrong.

    :param func: Pass the function that is being wrapped
    :return: The response of the function it decorates
    """

    async def async_inner(*args, **kwargs):
        db_obj: AsyncSession = kwargs.get("db_obj")
        if db_obj is None:
            raise ValueError("Database session 'db_obj' is required in the arguments.")

        try:
            response = await func(*args, **kwargs)
            await db_obj.commit()
            return response
        except Exception as database_exception:
            await db_obj.rollback()
            raise database_exception
        finally:
            await db_obj.close()

    def inner(*args, **kwargs):
        db_obj = kwargs.get("db_obj")
        if db_obj is None:
            raise ValueError("Database session 'db_obj' is required in the arguments.")

        try:
            response = func(*args, **kwargs)
            db_obj.commit()
            return response
        except Exception as database_exception:
            db_obj.rollback()
            raise database_exception
        finally:
            db_obj.close()

    if asyncio.iscoroutinefunction(func):
        return async_inner
    else:
        return inner
