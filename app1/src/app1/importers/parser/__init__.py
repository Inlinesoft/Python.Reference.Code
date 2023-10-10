import os

import boto3
from aws_lambda_powertools import Logger

from . import file_parser
from .myfile import MyFileParser

logger = Logger(child=True)

s3_client = boto3.client("s3", region_name=os.environ["API_REGION"])

@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    """
    serverless invoke local -f wmr-s3-parser
    --path pricers-etl/src/pricers_etl/
    importers/testEvents/wmrFile.json
    """
    main(event, file_parser)


def get_file_from_s3(sourcekey):
    sourcebucket = os.environ.get("S3_PRICING_DATA_BUCKET")

    # Download the file to /tmp/ folder
    file_name = os.path.basename(sourcekey)
    download_path = "/tmp/" + file_name  # nosec
    logger.info(
        f"sourcebucket {sourcebucket},  sourcekey {sourcekey}"
        + f" download_path {download_path}"
    )

    s3_client.download_file(sourcebucket, sourcekey, download_path)

    return download_path, file_name


def main(event, parser):
    sourcebucket = os.environ.get("S3_PRICING_DATA_BUCKET")
    sourcekey = event["Records"][0]["s3"]["object"]["key"]

    # allows lambda function to either be invoken with file name
    # ../2021/04/28/20210428_DJUBSCI_ccr.csv
    # or folder
    # .../2021/04/28/
    for key in s3_client.list_objects(Bucket=sourcebucket, Prefix=sourcekey)[
        "Contents"
    ]:
        file_path, file_name = get_file_from_s3(key["Key"])
        logger.info(f"File downloaded {file_path}")
        try:
            parser.execute(event, file_name, file_path)
        except ValueError as exe:
            logger.error(exe)
