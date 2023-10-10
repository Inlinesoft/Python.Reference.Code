import os
from decimal import Decimal

import jwt
import requests
from aws_lambda_powertools import Logger
from requests.auth import HTTPBasicAuth

logger = Logger(child=True)

uids = os.environ["API_USERNAME"].split(",")
pwds = os.environ["API_PASSWORD"].split(",")


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def get_auth(user: dict):
    if "auth_token" in user:
        return BearerAuth(user["auth_token"])

    uid = user.get("username", uids[0])
    upwd = ""
    try:
        idx = uids.index(uid)
        upwd = pwds[idx]
    except (ValueError, IndexError):
        pass

    return HTTPBasicAuth(uid, upwd)


def get_user_from_session(session):
    auth = session.auth
    if isinstance(auth, BearerAuth):
        decoded = jwt.decode(auth.token, verify=False)
        return decoded["email"]
    elif isinstance(auth, HTTPBasicAuth):
        return auth.username
    else:
        return "Not authenticated."


def get_session(event):
    sess = requests.Session()
    auth = get_auth(event.get("auth", {}))
    sess.auth = auth
    return sess


def get_base_url():
    host = os.environ.get("API_URL", "")
    base_url = "/".join([host, os.environ["API_STAGE"]])
    return base_url


def function1(product_code, payload, session, base_url):
    url = "/".join([base_url, "holidays", product_code, "12-12-02"])

    logger.info(f"POST {url} - {payload}")
    resp = session.post(url, json=payload)
    logger.info(f"{resp.status_code}, {payload['run_date']}, {product_code}")
    return resp


def get_holiday(session, holiday_date, holiday_type, holiday_reference):
    url = (
        f"{get_base_url()}/holidays/{holiday_date}"
        f"/{holiday_type}/{holiday_reference}"
    )
    resp = session.get(url)
    if resp.status_code != 200:
        return False
    data = resp.json()
    return data
