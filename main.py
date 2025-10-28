"""Entrypoint of the API"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from src.api import (
    user_role,
    user,
    user_authenticate,
    contact_us,
    customer_details,
    size,
    category,
    subcategory,
    category_xref,
    product,
    subproduct,
    color,
    review,
    wishlist,
    checkout,
    order,
    payment,
    healthcheck,
    version,
)
import uvicorn
from src.exceptions.user import (
    UserNotFound,
    UnauthorizedUser,
    UserIdMissing,
    UserEmailNotFound,
)
from fastapi.responses import JSONResponse
import json
from src.utils.utils import error_loc
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from src.exceptions.userrole import UserRoleNotFound, UserRoleExist, InvalidUserRole
from src.exceptions.customer_detail import CustomerDetailNotFound
from src.exceptions.contact_us import ContactUsNotFound
from src.exceptions.size import SizeNotFound, SizeAlreadyExists
from src.exceptions.category import CategoryNotFound, CategoryAlreadyExists
from src.exceptions.subcategory import SubcategoryNotFound
from src.exceptions.category_xref import CategoryXrefSubcategoryNotFound
from src.exceptions.order import OrderNotFound, UserOrderNotFound
from src.exceptions.checkout import (
    EmptyCartError,
    CartNotFound,
    CarttProductAlreadyExists,
    CartDeletionUnauthorizedUser,
    EmptyCart,
)
from src.exceptions.payment import PaymentNotFound
from src.middleware.middleware import RequestLoggingMiddleware
from src.exceptions.review import ReviewNotFound
from src.exceptions.wishlist import WishlistNotFound, WishlistProductAlreadyExists
from src.exceptions.subproduct import SubproductNotFound
from src.exceptions.product import ProductNotFound
from src.exceptions.user_authentication import (
    InvalidPassword,
    MissingAccessToken,
    MissingRefreshToken,
    InvalidOrExpiredToken,
    ExpiredToken,
    InvalidOTP,
    OTPExpired,
    FailedMail,
)

app = FastAPI()
app.add_middleware(RequestLoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_role.router)
app.include_router(user.router)
app.include_router(user_authenticate.router)
app.include_router(contact_us.router)
app.include_router(customer_details.router)
app.include_router(size.router)
app.include_router(category.router)
app.include_router(subcategory.router)
app.include_router(category_xref.router)
app.include_router(product.router)
app.include_router(subproduct.router)
app.include_router(color.router)
app.include_router(review.router)
app.include_router(wishlist.router)
app.include_router(checkout.router)
app.include_router(order.router)
app.include_router(payment.router)
app.include_router(healthcheck.router)
app.include_router(version.router)


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    errors = exc.errors()
    formatted_errors = [
        {"field": error_loc(error["loc"]), "message": error["msg"]} for error in errors
    ]
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message": "400 Bad Request",
            "description": "Request is not valid. Please check request body.",
            "errors": formatted_errors,
        },
    )


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """Custom exception handler for validation errors.
    This handler will be called when a RequestValidationError is raised.
    """
    errors = json.loads(exc.json())
    return JSONResponse(
        status_code=400,
        content={
            "message": "400 Bad Request",
            "description": "Request is not valid. Please check request body.",
            "errors": [
                {"field": error_loc(error["loc"]), "message": error["msg"]}
                for error in errors
            ],
        },
    )


@app.exception_handler(UserNotFound)
async def user_not_found_exception(request: Request, exception: UserNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "message": "404 Not Found",
            "description": exception.message,
        },
    )


@app.exception_handler(UserRoleNotFound)
async def user_role_not_found_exceptions(request: Request, exc: UserRoleNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "404 Not Found", "content": exc.message},
    )


@app.exception_handler(UserRoleExist)
async def user_role_exist_exceptions(request: Request, exc: UserRoleExist):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message": "400 Bad Request",
            "content": exc.message,
        },
    )


@app.exception_handler(InvalidUserRole)
async def invalid_user_role_exceptions(request: Request, exc: InvalidUserRole):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": "422 Unprocessable data",
            "content": exc.message,
        },
    )


@app.exception_handler(CustomerDetailNotFound)
async def customer_detail_not_found_exceptions(
    request: Request, exc: CustomerDetailNotFound
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "404 Not Found", "content": exc.message},
    )


@app.exception_handler(ContactUsNotFound)
async def contact_us_not_found_exceptions(request: Request, exc: ContactUsNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "404 Not Found", "content": exc.message},
    )


@app.exception_handler(UnauthorizedUser)
async def unauthorized_user_exceptions(request: Request, exc: UnauthorizedUser):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": "401 Unauthorized", "content": exc.message},
    )


@app.exception_handler(SizeNotFound)
async def size_not_found_exceptions(request: Request, exc: SizeNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "404 Not Found", "content": exc.message},
    )


@app.exception_handler(SizeAlreadyExists)
async def size_already_exists_exceptions(request: Request, exc: SizeAlreadyExists):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message": "400 Bad Request",
            "content": exc.message,
        },
    )


@app.exception_handler(CategoryNotFound)
async def category_not_found_exceptions(request: Request, exc: CategoryNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "404 Not Found", "content": exc.message},
    )


@app.exception_handler(CategoryAlreadyExists)
async def category_already_exists_exceptions(
    reuqest: Request, exc: CategoryAlreadyExists
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message": "400 Bad Request",
            "content": exc.message,
        },
    )


@app.exception_handler(SubcategoryNotFound)
async def subcategory_not_found_exceptions(request: Request, exc: SubcategoryNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "message": "404 Not Found",
            "content": exc.message,
        },
    )


@app.exception_handler(CategoryXrefSubcategoryNotFound)
async def category_xref_subcategory_not_found_exceptions(
    request: Request, exc: CategoryXrefSubcategoryNotFound
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "message": "404 Not Found",
            "content": exc.message,
        },
    )


@app.exception_handler(OrderNotFound)
async def order_not_found_exceptions(request: Request, exc: OrderNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "message": "404 Not Found",
            "content": exc.message,
        },
    )


@app.exception_handler(EmptyCartError)
async def empty_cart_exceptions(request: Request, exc: EmptyCartError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "message": "404 Not Found",
            "content": exc.message,
        },
    )


@app.exception_handler(ReviewNotFound)
async def review_not_found_exceptions(request: Request, exc: ReviewNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "404 Not Found", "content": exc.message},
    )


@app.exception_handler(CartNotFound)
async def cart_not_found_exceptions(request: Request, exc: CartNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "404 Not Found", "content": exc.message},
    )


@app.exception_handler(CarttProductAlreadyExists)
async def cart_exist_exceptions(request: Request, exc: CarttProductAlreadyExists):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message": "400 Bad Request",
            "content": exc.message,
        },
    )


@app.exception_handler(UserIdMissing)
async def user_id_missing_exceptions(request: Request, exc: UserIdMissing):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message": "400 Bad Request",
            "content": exc.message,
        },
    )


@app.exception_handler(CartDeletionUnauthorizedUser)
async def cart_deletion_authorization_exceptions(
    request: Request, exc: CartDeletionUnauthorizedUser
):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": "401 Unauthorized", "content": exc.message},
    )


@app.exception_handler(EmptyCart)
async def empty_cart_exceptions(request: Request, exc: EmptyCart):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "message": "404 Not Found",
            "content": exc.message,
        },
    )


@app.exception_handler(PaymentNotFound)
async def payment_not_found_exception(request: Request, exception: PaymentNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "message": "404 Not Found",
            "description": exception.message,
        },
    )


@app.exception_handler(WishlistNotFound)
async def wishlist_not_found_exceptions(request: Request, exc: WishlistNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "message": "404 Not Found",
            "content": exc.message,
        },
    )


@app.exception_handler(WishlistProductAlreadyExists)
async def wishlist_already_exists_exceptions(
    reuqest: Request, exc: WishlistProductAlreadyExists
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message": "400 Bad Request",
            "content": exc.message,
        },
    )


@app.exception_handler(ProductNotFound)
async def product_not_found_exception(request: Request, exception: ProductNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "message": "404 Not Found",
            "description": exception.message,
        },
    )


@app.exception_handler(SubproductNotFound)
async def subproduct_not_found_exception(
    request: Request, exception: SubproductNotFound
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "message": "404 Not Found",
            "description": exception.message,
        },
    )


@app.exception_handler(UserEmailNotFound)
async def user_email_not_found_exception(
    request: Request, exception: UserEmailNotFound
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "message": "404 Not Found",
            "description": exception.message,
        },
    )


@app.exception_handler(InvalidPassword)
async def invalid_password_exception(request: Request, exception: InvalidPassword):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "message": "401 Unauthorized",
            "description": exception.message,
        },
    )


@app.exception_handler(MissingAccessToken)
async def missing_access_token_exception(
    request: Request, exception: MissingAccessToken
):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "message": "401 Unauthorized",
            "description": exception.message,
        },
    )


@app.exception_handler(InvalidOrExpiredToken)
async def invalid_or_expired_token_exception(
    request: Request, exception: InvalidOrExpiredToken
):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "message": "401 Unauthorized",
            "description": exception.message,
        },
    )


@app.exception_handler(ExpiredToken)
async def expired_token_exception(request: Request, exception: ExpiredToken):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "message": "401 Unauthorized",
            "description": exception.message,
        },
    )


@app.exception_handler(OTPExpired)
async def otp_expired_exception(request: Request, exception: OTPExpired):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "message": "401 Unauthorized",
            "description": exception.message,
        },
    )


@app.exception_handler(InvalidOTP)
async def invalid_otp_exception(request: Request, exception: InvalidOTP):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "message": "401 Unauthorized",
            "description": exception.message,
        },
    )


@app.exception_handler(FailedMail)
async def failed_email_sending_exception(request: Request, exception: FailedMail):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "message": "503 Service unavailable.",
            "description": exception.message,
        },
    )


@app.exception_handler(UserOrderNotFound)
async def user_order_details_not_found_exception(
    request: Request, exception: UserOrderNotFound
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "message": "404 Not Found",
            "description": exception.message,
        },
    )


@app.exception_handler(MissingRefreshToken)
async def missing_refresh_token_exception(
    request: Request, exception: MissingRefreshToken
):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "message": "401 Unauthorized",
            "description": exception.message,
        },
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
