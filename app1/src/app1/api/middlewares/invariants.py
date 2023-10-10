import logging
import traceback

from fastapi import Request, status
from fastapi.responses import JSONResponse

from loader.application.use_cases import exceptions

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def catch_all_invariants(request: Request, call_next):
    try:
        response = await call_next(request)
    except exceptions.ResourceNotFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Resource not found"},
        )
    except exceptions.ResourceAlreadyExists:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": "Resource already found"},
        )
    except exceptions.ApplicationValidationError as exc:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Validation Error", "detail": str(exc)},
        )
    except exceptions.UncaughtApplicationError as exc:
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Server Error", "detail": str(exc)},
        )
    return response
