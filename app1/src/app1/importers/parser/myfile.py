# import os
import csv
from datetime import datetime

from aws_lambda_powertools import Logger

from pricers_etl.services import api

from ..utils import extract_table_csv
from .parser_base import ParserBase

logger = Logger(child=True)


class MyFiler(ParserBase):
    file_patterns = [
        (
            r"wmr(0[1-9]|[12][0-9]|3[01])(0[1-9]|1[012])",
            None,
        ),
    ]

 
    def _row_to_entity(self, row, data_date, currency_froms, currency_to):
        currency_from = row["ISO"]
        if currency_from not in currency_froms:
            logger.info(f"Skipping currency_from {currency_from}")
            return
        row_data_date = datetime.strptime(
            row["Date & Time"], "%d/%m/%Y %H:%M"
        ).date()
        if data_date != row_data_date:
            logger.error(
                f"WMR Rates Parsing issue where header data_date {data_date} "
                f"not matching with row data_date - {row_data_date}"
            )
        return {
            "provider_type": self._get_provider_type(),
            "currency_from": currency_from,
            "currency_to": currency_to,
            "rate_type": self._get_rate_type(),
            "data_date": data_date.isoformat(),
            "ask": row[f"{currency_to} Ask"],
            "bid": row[f"{currency_to} Bid"],
            "mid": row[f"{currency_to} Mid"],
            "divisor": 1,
            "reason": self.reason,
        }

    def get_data_date(self, file_path):
        with open(file_path) as f:
            lines = f.readlines()
            # Parses the 2nd line in csv to identify the date
            file_date = datetime.strptime(
                lines[1].split(",")[0][-10:], "%d/%m/%Y"
            ).date()
            return file_date

    def run(self, file_path):
        logger.info(f"Calling parser WMR Spot Rates for {file_path}")

        data_date = self.get_data_date(file_path)

        with open(file_path, newline="") as csvfile:
            file_reader = csv.reader(csvfile)
            _, rows = extract_table_csv(file_reader, header_row_index=2)

            for row in rows:
                entity = self._row_to_entity(
                    row, data_date, currency_froms, currency_to
                    )
                if entity:
                    logger.info(f"POST rates value {entity}")
                    api.insert_data(
                        self.session, entity, force=self.force
                    )
