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



def get_product(product_code, session, base_url):
    url = "/".join([base_url, "products", product_code])
    resp = session.get(url)
    logger.info(f"get_product {resp.status_code}, {url}")
    return resp


def get_products(session, base_url):
    url = "/".join([base_url, "products"])
    resp = session.get(url)
    logger.info(f"get_products {resp.status_code}, {url}")
    return resp

def insert_shares(session, data, force=False):
    url = (
        f'{get_base_url()}/shares-outstanding/{data["product_code"]}'
        f'/{data["trade_date"]}'
    )
    logger.info(f'Inserting shares outstanding {data["product_code"]} {url}')

    data.pop("product_code")
    data.pop("trade_date")
    response = session.post(url, json=data)
    logger.info(f"Response: {response.status_code}")
    if response.status_code == 409:
        logger.info(f"Data entry exists. force? {force}")
        if force:
            response = session.put(url, json=data)
            if response.status_code != 200:
                logger.error(
                    f"Update shares outstanding failed - {response.json()}"
                )
            else:
                logger.info(
                    f"Shares outstanding data updated: {response.status_code}"
                )
        else:
            logger.warning("Conflict inserting shares outstanding data")
    elif response.status_code == 201:
        logger.info("Data entry inserted")
    else:
        logger.error(
            f"Inserting shares outstanding data failed: {response.json()}"
        )


def insert_rates(session, data, force=False):
    url = (
        f"{get_base_url()}/forex-rates"
        f'/{data["provider_type"]}'
        f'/{data["currency_from"]}'
        f'/{data["currency_to"]}'
        f'/{data["rate_type"]}'
        f'/{data["data_date"]}'
    )
    logger.info(f'Inserting forex_rates {data["data_date"]} {url}')

    data.pop("currency_from")
    data.pop("currency_to")
    data.pop("rate_type")
    data.pop("data_date")
    response = session.post(url, json=data)
    logger.info(f"Response: {response.status_code}")
    if response.status_code == 409:
        logger.info(f"Data entry exists. force? {force}")
        if force:
            response = session.put(url, json=data)
            if response.status_code != 200:
                logger.error(f"Update forex_rates failed - {response.json()}")
            else:
                logger.info(
                    f"forex_rates data updated: {response.status_code}"
                )
        else:
            logger.warning("Conflict inserting forex_rates data")
    elif response.status_code == 201:
        logger.info("Data entry inserted")
    else:
        logger.error(f"Inserting forex_rates data failed: {response.json()}")




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
