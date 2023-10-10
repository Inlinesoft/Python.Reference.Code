import os
from datetime import date
from decimal import Decimal

import pyodbc
from aws_lambda_powertools import Logger

logger = Logger(child=True)

conn = None


def get_connection():
    global conn
    print("conn", type(conn), conn)
    if conn is None:
        print("server:", os.environ.get("DB_SERVER", ""))
        aux = pyodbc.connect(
            "DRIVER={ODBC Driver 13 for SQL Server};"
            f'SERVER={os.environ.get("DB_SERVER", "")};'
            f'DATABASE={os.environ.get("DB_DATABASE", "")};'
            f'UID={os.environ.get("DB_USER", "")};'
            f'PWD={os.environ.get("DB_PASSWORD", "")}'
        )
        conn = aux

    return conn


def get_product_id(product_code):
    res = None
    sql = (
        "select ProductId as product_id from ExchangeProduct"
        " where ExchangeCode = ?"
        " and (IsDeleted = 0 or ExchangeCode IN ('ETHW'))"
    )
    rows = get_data_from_db(sql, (product_code,))
    res = None
    if rows:
        res = rows[0]["product_id"]

    logger.info(f"Product - {product_code} Id - {res}")
    return res


def get_data_from_db(sql, params=()):
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        logger.debug(f"The SQL to execute is {sql}")
        cur.execute(sql, params)
    except pyodbc.Error as exc:
        logger.error(
            f"encountered error when fetching data from central db - {exc}"
        )
    else:
        logger.info("Executed SQL")
        res = []
        columns = [column[0] for column in cur.description]

        def stringify(value):
            if isinstance(value, Decimal):
                return str(value)
            elif isinstance(value, date):
                return value.isoformat()
            else:
                return value

        for row in cur:
            items = [stringify(x) for x in row]
            d = dict(zip(columns, items))
            res.append(d)

        logger.info(f"Got {len(res)} items from central db")
        return res
    finally:
        cur.close()
