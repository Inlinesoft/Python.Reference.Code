import logging
import time

from fastapi import Request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def log_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Process-Time"] = str(process_time)
    try:
        user = request.state.user
    except AttributeError:
        user = "unknown"

    try:
        endpoint_name = request.scope["endpoint"].__name__
    except (KeyError, AttributeError):
        endpoint_name = ""
    payload = {
        "username": user,
        "response_code": response.status_code,
        "base_url": request.base_url.hostname,
        "path": request.scope["path"],
        "endpoint_name": endpoint_name,
        "path_params": request.path_params,
        "query_params": request.query_params.multi_items(),
        "method": request.method,
        "client_address": request.scope["client"],
        "server_address": request.scope["server"],
        "duration_in_ms": process_time,
    }
    logger.info(f"Metrics payload {payload}")
    return response
