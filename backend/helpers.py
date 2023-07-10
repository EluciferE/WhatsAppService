from functools import wraps
from starlette import status
from starlette.responses import JSONResponse
import logging


def catch_server_error(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as error:
            logging.error(error)
            return JSONResponse(
                {"message": str(error)},
                status_code=getattr(error, '_STATUS_CODE', status.HTTP_500_INTERNAL_SERVER_ERROR)
            )

    return wrapper
