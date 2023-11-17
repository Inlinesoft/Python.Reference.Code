import jwt
import pyodbc
from aws_lambda_powertools import Logger

from ..helpers import constants
from ..services import api
from ..services.db import get_connection

logger = Logger()


def insert(
    conn, product_id, data_date, coins_in_custody, user
):
    upd_stmt = (
        "UPDATE table1"
        " SET IsDeleted = 1,"
        " ModifiedBy = ?, ModifiedOn = GETDATE()"
        " WHERE IsDeleted = 0"
        " AND ProductId = ? AND DataDate = ?"
    )
    insert_stmt = (
        "INSERT INTO table2"
        " (ProductId, DataDate, CoinsInCustody,"
        " CreatedBy, ModifiedBy)"
        " VALUES (?, ?, ?, ?, ?)"
    )
    by_whom = f"{user} - {constants.USER}"
    try:
        cur = conn.cursor()
        cur.execute(upd_stmt, by_whom, product_id, data_date)
        cur.execute(
            insert_stmt,
            product_id,
            data_date,
            coins_in_custody,
            by_whom,
            by_whom,
        )
        return True
    except pyodbc.Error as exc:
        logger.error(
            f"encountered error when publishing data to central db - {exc}"
        )
        return False
    finally:
        cur.close()


def publish(product_code, data_date, coins_in_custody, user):
    error_resp = {
        "status": "failure",
        "message": "Application error. Please contact IT Team",
    }
    resp = {}
    try:
        product_id = get_product_id(product_code)
        conn = get_connection()
        res = insert(
            conn, product_id, data_date, coins_in_custody, user
        )
        if res:
            msg = (
                f"successfully published coins_in_custody {coins_in_custody} "
                f"to CDB for {product_code} and date {data_date}"
            )
            logger.info(msg)
            resp = {"status": "success", "message": msg}
            conn.commit()
        else:
            resp = error_resp
        # I get connection closed error when I run this repeatedly locally.
        # Need to test this in lamdba environment to confirm behaviour
        # conn.close()
    except Exception as exc:
        logger.error(exc)
        resp = error_resp
        resp["detail"] = str(exc)
    return resp


def get_user_from_event(event):

    auth = event.get("auth", {})
    if "auth_token" in auth:
        decoded = jwt.decode(auth["auth_token"], verify=False)
        print(decoded)
        return "token"

    return auth.get("username", "anon user")


@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    sess = api.get_session(event)
    base_url = api.get_base_url()
    product = event["product_code"]
    resp = api.get_product(product, sess, base_url)
    product = resp.json()

    res = {}

    if resp.status_code != 200:
        msg = (
            f"{product}  "
            f"{resp.status_code} - {product}"
        )
        logger.error(msg)
        res = {"status": "failure", "message": msg}

    else:
        user = get_user_from_event(event)
        res = publish(product_code, user)
    return res
