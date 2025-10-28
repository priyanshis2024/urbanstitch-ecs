from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from src.middleware.logger import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        logger.info(
            f"{request.client.host},{request.method},{request.url.path},{response.status_code}"
        )
        return response
