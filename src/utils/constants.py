"""This file contains the constants"""

from enum import Enum


class Role(int, Enum):
    ADMIN = 1
    USER = 2
    TEMP = 3
    SYSTEM_USER = 4


class Status(int, Enum):
    DISABLED = 1
    ENABLED = 2
    BLOCKED = 3


class UuidPrefix(str, Enum):
    USER = "user:"
    CUSTOMER = "customer:"


class OrderStatus(int, Enum):
    PENDING = 1
    CONFIRMED = 2
    FAILED = 3
    DISPATCHED = 4
    INTRANSMIT = 5
    OUT_FOR_DELIVERY = 6
    CANCELLED = 7
    DELIVERED = 8
    COMPLETED = 9
    SHIPED = 10


class PaymentStatus(int, Enum):
    INITIATED = 1
    CANCELLED = 2
    SUCCESS = 3
    FAILED = 4
    REFUND_INITIATED = 5
    REFUND_SUCCESS = 6
    REFUND_FAILED = 7


class RequestValidationErrorMessage:
    VALIDATE_PASSWORD = "Invalid Password. Password must be at least 8 characters long, starts with character from A-Z or a-z and contain at least one letter from A-Z, a-z, one number from 0-9 and special character like #,$,!,%,@,&,*."
    VALIDATE_EMAIL = "Invalid Email. Email must contain '@' and '.' and should not contain any special characters."
    VALIDATE_PHONE_NUMBER = "Invalid Phone Number. Contact number should be 10 digits long and start with 6, 7, 8 or 9."
    VALIDATE_DATE = "Invalid Date. Future date should not be allowed."
    VALIDATE_NAME = "{value} only contains alphabets. Numbers and special characters are not allowed."


class ErrorMessage:
    USER_NOT_FOUND = "User info with user id '{user_id}' not found in the system."
    USER_ROLE_NOT_FOUND = "User role with id '{user_role_id}' not found in the system."
    USER_ROLE_ALREADY_EXISTS = (
        "User role with id '{user_role_id}' already exists in the system."
    )
    INVALID_USER_ROLE = (
        "Invalid user role id '{user_role_id}'. User role must be between the range."
    )
    CUSTOMER_DETAIL_NOT_FOUND = (
        "Customer with id '{customer_detail_id}' not found in the system."
    )
    CONTACT_US_NOT_FOUND = (
        "Contact us details with id '{contact_us_id}' not found in the system."
    )
    UNAUTHORIZED_USER = "Unauthorized user. User with id '{user_id}' is not authorized user to access this resource."
    SIZE_NOT_FOUND = "Size with id '{size_id}' not found in the system."
    SIZE_ALREADY_EXISTS = "Size with id '{size_id}' already exists in the system."
    CATEGORY_NOT_FOUND = "Category with id '{category_id}' not found in the system."
    SUBCATEGORY_NOT_FOUND = (
        "Subcategory with id '{subcategory_id}' not found in the system."
    )
    CATEGORY_XREF_SUBCATEGORY_NOT_FOUND = (
        "Category with id '{category_id}' does not have subcategories in the system."
    )
    CATEGORY_ALREADY_EXISTS = (
        "Category with id '{category_id}' already exists in the system."
    )
    ORDER_NOT_FOUND = "Order with id '{order_id}' not found in the system."
    EMPTY_CART_FOUND = (
        "Order creation failed: Please add items before placing an order."
    )
    CART_NOT_FOUND = "Cart with id '{cart_id}' not found in the system."
    CART_ALREADY_EXISTS = (
        "Cart with subproduct id '{subproduct_id}' already exists in the system."
    )
    USER_ID_MISSING = "User id is missing."
    CART_DELETION_AUTHORIZATION = (
        "User {user_id} is not authorized to delete cart {cart_id}"
    )
    CART_EMPTY = "Cart is already empty."
    PAYMENT_NOT_FOUND = "Payment with id '{payment_id}' not found in the system."
    REVIEW_NOT_FOUND = "Review with id '{review_id}' not found in the system."
    WISHLIST_NOT_FOUND = "Wishlist with id '{wishlist_id}' not found in the system."
    WISHLIST_ALREADY_EXISTS = (
        "Wishlist with subproduct id '{subproduct_id}' already exists in the system."
    )
    SUBPRODUCT_NOT_FOUND = (
        "Subproduct with id '{subproduct_id}' not found in the system."
    )

    PRODUCT_NOT_FOUND = (
        "Product info with product id '{product_id}' not found in the system."
    )
    USER_EMAIL_NOT_FOUND = "User info with email '{email}' not found in the system."
    INVALID_PASSWORD = "Invalid password. Please try again."
    INVALID_OR_EXPIRED_TOKEN = "Invalid or expired token."
    ACCESS_TOKEN_MISSING = "Please provide an access token"
    REFRESH_TOKEN_MISSING = "Please provide a refresh token"
    EXPIRED_TOKEN = "Your token is expired you cannot used to access protected routes"
    FAILED_SENDING_EMAIL = "Failed to send email."
    USER_ORDER_NOT_FOUND = "Order with user id '{user_id}' not found in the system."


class Message:
    LOGIN_SUCCESS = "Login Successful"
    INVALID_OTP = "Invalid OTP"
    OTP_EXPIRED = "OTP not found or expired."
    FAILED_SENDING_EMAIL = "Failed to send email."
    OTP_SUCCESS_MESSAGE = "OTP sent successfully to your email."
    OTP_VERIFICATION_MESSAGE = "OTP verification is successful."
    OVERRIDE_SUBCLASS = "Please override this method in the subclass."


class Currency:
    INR = "inr"


class PaymentMethod(int, Enum):
    CARD = 1
    COD = 2
    LINK = 3
    UPI = 4


class StripeMode:
    PAYMENT = "payment"
    SUBSCRIPTION = "subscription"
    SETUP = "setup"


class SmtpServerTimeout:
    TIMEOUT = 10


class ProductTax:
    TAX = 2.5
    PAISA = 100


class EmailSubjects:
    OTP_SUBJECT = "Your OTP Code"
    ORDER_INVOICE_SUBJECT = "Order Invoice"


class StripeStatus:
    REFUND_SUCCESS_STATUS = "success"
