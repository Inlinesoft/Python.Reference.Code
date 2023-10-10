import datetime

from pricers_etl.services import api


def _is_empty_row(row):
    return all(not value for value in row.values())


def _is_empty_list(header_row):
    return all(not value for value in header_row)


def extract_table_xlrd(
    sheet,
    header_row_index,
    max_row_index=None,
    find_header=False,
    overwrite_headers=False,
):
    """
    Extract a table from xls file:
        header_row_index:
            int (start of the table scan, unless find_header is True)
        max_row_index:
            int (default: None)
            (if provided, will stop table scan at this row index)
        find_header:
            bool (if True, will assume heder row to be
                  first non empty row after header_row_index)
    """
    headers = [cell.value for cell in sheet.row(header_row_index)]
    if find_header:
        while _is_empty_list(headers):
            header_row_index = header_row_index + 1
            headers = [cell.value for cell in sheet.row(header_row_index)]

    result_rows = []
    last_row_index = header_row_index + 1

    for row_idx in range(last_row_index, sheet.nrows):  # Iterate through rows
        row = [cell.value for cell in sheet.row(row_idx)]
        if _is_empty_list(row):
            break
        values = {}
        merged_headers_row = zip(headers, row)
        if overwrite_headers:
            merged_headers_row = zip(overwrite_headers, row)

        for key, cell_value in merged_headers_row:
            values[key] = cell_value

        result_rows.append(values)
        last_row_index = last_row_index + 1

    return headers, result_rows, last_row_index


def extract_table_csv(
    reader, header_row_index, max_row_index=None, find_header=False
):
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

