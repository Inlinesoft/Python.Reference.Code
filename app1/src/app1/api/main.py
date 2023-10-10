import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from mangum import Mangum

import loader
from loader.infrastructure.services.db import configure_dependencies

from . import (
    holidays,
   
)
from .config import Config
from .security import User, get_current_user, load_jwks


def get_prefix():
    res = ""
    api_stage = Config.API_STAGE
    if api_stage:
        res = "/" + api_stage
    return res


app = FastAPI(
    title="Pricing API",
    description="Pricing REST API for streamlined interactions",
    version=loader.__version__,
    openapi_url=get_prefix() + "/openapi.json",
    root_path=get_prefix(),
)

# https://ui.capmarkets.io/
# https://ui.tech.io/
origins = Config.API_CORS_ORIGINS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=500)
app.middleware("http")(middlewares.catch_all_invariants)
app.middleware("http")(middlewares.log_metrics)


@app.on_event("startup")
def on_start_up():
    configure_dependencies()
    load_jwks()


@app.get("/users/me")
def read_current_user(user: User = Depends(get_current_user)):
    return {"username": user.username, "groups": user.groups}


app.include_router(
    operations.router,
    prefix="/operations",
    tags=["Operations"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    holidays.router,
    prefix="/holidays",
    tags=["Holidays"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)


handler = Mangum(app, log_level="warning")


def run():
    host = Config.API_HOST
    port = Config.API_PORT
    uvicorn.run(app, host=host, port=port)


# if __name__ == "__main__":
#     run()


# GET /holidays/<issuer>
# POST /holidays
# PUT /holidays/issuer-id
# DELETE /holidays/issuer-id
