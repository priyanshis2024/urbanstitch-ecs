from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, func, ForeignKey, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, JSON, REAL, ARRAY, FLOAT
from sqlalchemy.orm import relationship
from src.utils.utils import generate_random_uuid, attach_prefix_to_uuid
from src.utils.constants import UuidPrefix, OrderStatus, PaymentMethod

import uuid

Base = declarative_base()


class Size(Base):
    __tablename__ = "sizes"
    __table_args__ = {"schema": "products"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=generate_random_uuid,
    )
    size = Column(String(1024), nullable=False)
    data = Column(JSON, nullable=False)
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
    created_by = Column(
        String,
        nullable=True,
        default=attach_prefix_to_uuid(input_uuid=uuid.uuid4(), prefix=UuidPrefix.USER),
    )
    updated_by = Column(
        String,
        nullable=True,
        default=attach_prefix_to_uuid(input_uuid=uuid.uuid4(), prefix=UuidPrefix.USER),
    )

    subproducts = relationship("Subproduct", back_populates="sizes")


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = {"schema": "products"}

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    status = Column(Integer, nullable=False, default=1)
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
    created_by = Column(
        String,
        nullable=True,
        default=attach_prefix_to_uuid(input_uuid=uuid.uuid4(), prefix=UuidPrefix.USER),
    )
    updated_by = Column(
        String,
        nullable=True,
        default=attach_prefix_to_uuid(input_uuid=uuid.uuid4(), prefix=UuidPrefix.USER),
    )

    category_xrefs = relationship("CategoryXref", back_populates="categories")


class Subcategory(Base):
    __tablename__ = "subcategories"
    __table_args__ = {"schema": "products"}

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    status = Column(Integer, nullable=False, default=1)
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
    created_by = Column(
        String,
        nullable=True,
        default=attach_prefix_to_uuid(input_uuid=uuid.uuid4(), prefix=UuidPrefix.USER),
    )
    updated_by = Column(
        String,
        nullable=True,
        default=attach_prefix_to_uuid(input_uuid=uuid.uuid4(), prefix=UuidPrefix.USER),
    )

    category_xrefs = relationship("CategoryXref", back_populates="subcategories")


class CategoryXref(Base):
    __tablename__ = "category_xrefs"
    __table_args__ = {"schema": "products"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=generate_random_uuid,
    )
    category_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.categories.id", ondelete="CASCADE"),
        nullable=False,
    )
    subcategory_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.subcategories.id", ondelete="CASCADE"),
        nullable=False,
    )
    subcategories_type = Column(String(255), nullable=False)

    categories = relationship(
        "Category", back_populates="category_xrefs", cascade="all, delete"
    )
    subcategories = relationship(
        "Subcategory", back_populates="category_xrefs", cascade="all, delete"
    )
    products = relationship("Product", back_populates="category_xrefs", uselist=False)


class Product(Base):
    """This class maps to a table user that holds
    the user details."""

    __tablename__ = "products"
    __table_args__ = {"schema": "products"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
    )
    category_xref_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.category_xrefs.id", ondelete="CASCADE"),
        nullable=False,
    )
    # brand_id = Column(UUID(as_uuid=True),ForeignKey('brand.brand.id', ondelete='CASCADE'), nullable=False)
    brand_id = Column(
        UUID(as_uuid=True),
        nullable=False,
        default="550e8400-e29b-41d4-a716-446655440000",
    )
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    data = Column(JSON, nullable=True)
    fabric = Column(String, nullable=True)
    price = Column(Integer, nullable=False)
    rating = Column(REAL, nullable=True, default=0)
    total_quantity = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False, default=1)
    thumbnail_image = Column(String, nullable=False)
    created_by = Column(
        String,
        nullable=True,
        default=attach_prefix_to_uuid(input_uuid=uuid.uuid4(), prefix=UuidPrefix.USER),
    )
    updated_by = Column(
        String,
        nullable=True,
        default=attach_prefix_to_uuid(input_uuid=uuid.uuid4(), prefix=UuidPrefix.USER),
    )
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

    category_xrefs = relationship(
        "CategoryXref", back_populates="products", uselist=False
    )
    subproducts = relationship(
        "Subproduct", back_populates="products", cascade="all, delete-orphan"
    )
    reviews = relationship(
        "Review", back_populates="products", cascade="all, delete-orphan"
    )


class Subproduct(Base):
    __tablename__ = "subproducts"
    __table_args__ = {"schema": "products"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
    )

    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.products.id", ondelete="CASCADE"),
        nullable=False,
    )
    size_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.sizes.id", ondelete="CASCADE"),
        nullable=True,
    )
    price = Column(Integer, nullable=False)
    color = Column(String(100), nullable=True)
    quantity = Column(Integer, nullable=False, default=0)
    images = Column(ARRAY(String), nullable=False)
    status = Column(Integer, nullable=False, default=1)
    created_by = Column(
        String(255),
        nullable=False,
        default=lambda: attach_prefix_to_uuid(
            input_uuid=uuid.uuid4(), prefix=UuidPrefix.USER
        ),
    )
    updated_by = Column(
        String(255),
        nullable=False,
        default=lambda: attach_prefix_to_uuid(
            input_uuid=uuid.uuid4(), prefix=UuidPrefix.USER
        ),
    )
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

    products = relationship("Product", back_populates="subproducts")
    sizes = relationship("Size", back_populates="subproducts")
    wishlists = relationship("Wishlist", back_populates="subproducts")
    carts = relationship("Cart", back_populates="subproducts")
    order_histories = relationship("OrderHistory", back_populates="subproducts")


class Review(Base):
    """This class maps to a table user that holds
    the user details."""

    __tablename__ = "reviews"
    __table_args__ = {"schema": "products"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=generate_random_uuid,
    )
    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.products.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = Column(
        String,
        nullable=False,
        default=lambda: attach_prefix_to_uuid(
            input_uuid=uuid.uuid4(), prefix=UuidPrefix.USER
        ),
    )
    rating = Column(Integer, nullable=True)
    review = Column(String(1024), nullable=True)
    image = Column(String(255), nullable=True)
    is_rated = Column(Integer, nullable=False, default=0)
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

    products = relationship("Product", back_populates="reviews")


class Wishlist(Base):
    __tablename__ = "wishlists"
    __table_args__ = {"schema": "products"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=generate_random_uuid,
    )
    user_id = Column(
        String,
        nullable=False,
        default=attach_prefix_to_uuid(input_uuid=uuid.uuid4(), prefix=UuidPrefix.USER),
    )
    subproduct_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.subproducts.id", ondelete="CASCADE"),
        nullable=False,
    )
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

    subproducts = relationship("Subproduct", back_populates="wishlists")


class Cart(Base):
    __tablename__ = "carts"
    __table_args__ = {"schema": "products"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=generate_random_uuid,
    )
    user_id = Column(
        String,
        nullable=False,
        default=attach_prefix_to_uuid(input_uuid=uuid.uuid4(), prefix=UuidPrefix.USER),
    )
    subproduct_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.subproducts.id", ondelete="CASCADE"),
        nullable=False,
    )
    order_quantity = Column(Integer, nullable=False)
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
    subproducts = relationship("Subproduct", back_populates="carts")


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {"schema": "products"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=generate_random_uuid,
    )
    user_id = Column(
        String,
        nullable=False,
        default=attach_prefix_to_uuid(input_uuid=uuid.uuid4(), prefix=UuidPrefix.USER),
    )
    customer_id = Column(
        String,
        nullable=False,
        default=attach_prefix_to_uuid(
            input_uuid=uuid.uuid4(), prefix=UuidPrefix.CUSTOMER
        ),
    )
    order_status = Column(Integer, default=OrderStatus.PENDING, nullable=False)
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
    order_histories = relationship("OrderHistory", back_populates="orders")
    payments = relationship(
        "Payment", back_populates="orders", uselist=False, cascade="all, delete-orphan"
    )


class OrderHistory(Base):
    __tablename__ = "order_histories"
    __table_args__ = {"schema": "products"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=generate_random_uuid,
    )
    order_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.orders.id", ondelete="CASCADE"),
        nullable=False,
    )
    subproduct_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.subproducts.id", ondelete="CASCADE"),
        nullable=False,
    )
    price = Column(Integer, nullable=False)
    order_quantity = Column(Integer, nullable=False)
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
    orders = relationship("Order", back_populates="order_histories")
    subproducts = relationship("Subproduct", back_populates="order_histories")


class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = {"schema": "products"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=generate_random_uuid,
    )
    order_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.orders.id", ondelete="CASCADE"),
        nullable=False,
    )
    amount = Column(FLOAT, nullable=False)
    payment_status = Column(Integer, nullable=False)
    transaction_id = Column(String, nullable=True)
    refund_id = Column(String, nullable=True)
    payment_method = Column(Integer, nullable=False, default=PaymentMethod.CARD)
    payment_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    orders = relationship("Order", back_populates="payments", uselist=False)
