import json
import logging
import os
import secrets
from typing import Dict, List, Optional

import jwt
import requests
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
)
from pydantic import BaseModel as ViewModel

from .config import Config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


securityBearer = HTTPBearer(auto_error=False)
securityBasic = HTTPBasic(auto_error=False)

# loads once on module load
public_keys: List[Dict] = []


def load_jwks():
    global public_keys
    if public_keys:
        return
    try:
        public_keys = requests.get(os.environ.get("OKTA_JWKS_URL", "")).json()[
            "keys"
        ]
    except Exception as exe:
        logger.warn(
            f'Could not load jwks from {os.environ.get("OKTA_JWKS_URL", "")}'
        )
        logger.info(exe)


class User(ViewModel):
    username: str
    password: Optional[str]
    groups: List[str] = []
    auth_token: Optional[str]


def basic_auth(request: Request, credentials: HTTPBasicCredentials):
    creds = Config.API_CREDENTIALS
    try:
        api_password = creds[credentials.username]
    except KeyError:
        correct_password = False
    else:
        correct_password = secrets.compare_digest(
            credentials.password, api_password
        )

    if not correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    else:
        request.state.user = credentials.username
    return User(username=credentials.username, password=credentials.password)


def bearer_auth(request: Request, credentials: HTTPAuthorizationCredentials):
    """
    # verify JWT ID token
    # if correct return user, otherwise rise exeption
    """
    try:
        kid = jwt.get_unverified_header(credentials.credentials)["kid"]
        jwk = [key for key in public_keys if key["kid"] == kid][0]
        key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

        payload = jwt.decode(
            credentials.credentials,
            key=key,
            audience=os.environ.get("OKTA_CLIENT_ID", ""),
            algorithms=["RS256"],
        )
    except Exception as exe:
        logger.info("bearer_auth failed")
        logger.info(str(exe))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return User(
        username=payload["email"],
        groups=[],
        auth_token=credentials.credentials,
    )


def get_current_user(
    request: Request,
    credentials_basic: HTTPBasicCredentials = Depends(securityBasic),
    credentials_bearer: HTTPAuthorizationCredentials = Depends(securityBearer),
):
    if credentials_basic is not None:
        # TODO: inject groups arr when using basic auth ?
        return basic_auth(request, credentials_basic)

    if credentials_bearer is not None:
        return bearer_auth(request, credentials_bearer)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect auth method.",
        headers={"WWW-Authenticate": "Basic/Bearer"},
    )
