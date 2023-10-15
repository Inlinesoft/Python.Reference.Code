# import os
import csv
from datetime import datetime

from aws_lambda_powertools import Logger

from pricers_etl.services import api

from ..utils import extract_table_csv
from .parser_base import ParserBase

logger = Logger(child=True)


class CSVParser(ParserBase):

    file_patterns = [
        (
            r"wmr(0[1-9]|[12][0-9]|3[01])(0[1-9]|1[012])",
            None,
        ),
    ]

    def __init__(self):
        super().__init__()

    
    def extract_file_data(self, file_path) -> list[dict]: # return type id list of dict
        logger.info(f"Calling parser WMR Spot Rates for {file_path}")

        data_date = self.get_data_date(file_path)

        with open(file_path, newline="") as csvfile:
            file_reader = csv.reader(csvfile)
            header, rows = extract_data(file_reader, header_row_index=2)

        return rows
    
    def extract_data(reader, header_row_index, max_row_index=None, find_header=False ):
        """
        Extract a table from csv file:
            header_row_index: int
                (start of the table scan, unless find_header is True)
            max_row_index: int (default: None)
                (if provided, will stop table scan at this row index)
            find_header: bool
                (if True, will assume heder row to be first
                non empty row after header_row_index)
        """
        headers = []
        result_rows = []

        for i, row in enumerate(reader):
            if i == header_row_index:
                headers = row

            if find_header:
                # placeholder for future impl.
                raise "Not implemented"

            # headers parser, row is now data row
            if i > header_row_index:
                values = {}
                for key, cell_value in zip(headers, row):
                    values[key] = cell_value
                result_rows.append(values)

            if max_row_index and i >= max_row_index:
                break

        return headers, result_rows
