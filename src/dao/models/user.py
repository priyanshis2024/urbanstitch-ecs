from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Date, Integer, Text, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, INTEGER
from sqlalchemy.orm import relationship
from src.utils.utils import generate_random_uuid

Base = declarative_base()


class UserRole(Base):
    """This class maps to a table user role that holds
    the user's role details."""

    __tablename__ = "user_roles"
    __table_args__ = {"schema": "users"}

    id = Column(INTEGER, primary_key=True, nullable=False)
    role = Column(String(255), nullable=False, default=2)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    users = relationship("User", back_populates="user_roles", uselist=True)


class User(Base):
    """This class maps to a table users that holds
    the users details."""

    __tablename__ = "users"
    __table_args__ = {"schema": "users"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=generate_random_uuid,
    )
    user_role_id = Column(
        INTEGER,
        ForeignKey("users.user_roles.id", ondelete="CASCADE"),
        nullable=False,
    )
    contact = Column(Text, nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    username = Column(String(100), nullable=True)
    image = Column(String(255), nullable=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    gender = Column(Integer, nullable=True)
    dob = Column(Date, nullable=True)
    status = Column(Integer, nullable=False)
    otp = Column(Text, nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    user_roles = relationship("UserRole", back_populates="users", uselist=False)
    customer_details = relationship("CustomerDetails", back_populates="users")
    contact_us = relationship("ContactUs", back_populates="users")
    user_authentications = relationship("UserAuthentications", back_populates="users")


class ContactUs(Base):
    """This class maps to a table contact us that holds
    the user details for the contacting to the portal."""

    __tablename__ = "contact_us_details"
    __table_args__ = {"schema": "users"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=generate_random_uuid,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.users.id", ondelete="CASCADE"),
        nullable=False,
    )
    message = Column(String(1024), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    users = relationship("User", back_populates="contact_us")


class CustomerDetails(Base):
    """This class maps to a table address that holds
    the user's address details."""

    __tablename__ = "customer_details"
    __table_args__ = {"schema": "users"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=generate_random_uuid,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.users.id", ondelete="CASCADE"),
        nullable=False,
    )
    contact = Column(Text, nullable=False)
    email = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    address_type = Column(Integer, nullable=False)
    address = Column(String(255), nullable=False)
    landmark = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    pincode = Column(Integer, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    users = relationship("User", back_populates="customer_details")


class UserAuthentications(Base):
    """This class maps to a table user authentication that holds
    the user's login token details."""

    __tablename__ = "user_authentications"
    __table_args__ = {"schema": "users"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=generate_random_uuid,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.users.id", ondelete="CASCADE"),
        nullable=False,
    )
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    expired_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
    )

    users = relationship("User", back_populates="user_authentications")
