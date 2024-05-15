from starlette.middleware.base import BaseHTTPMiddleware

from .logger import logger


class JSONAccessLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        logger.info(
            "Incoming request",
            extra={
                "req": {
                    "method": request.method,
                    "url": str(request.url),
                    "client": str(request.client.host),
                    "user-agent": request.headers.get("user-agent", "N/A"),
                },
                "res": {
                    "status_code": response.status_code,
                },
            },
        )
        return response
