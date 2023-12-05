from datetime import timedelta
from decimal import Decimal

import pytest

from application.use_cases import (
    GenStatsUseCase,
    ReportStatsUseCase,
    exceptions,
)


class Helpers:
    @staticmethod
    def run_pricing(start_date, end_date, product_code, force=False):
        use_case = GenStatsUseCase()

        run_date = start_date
        end_date = end_date

        while run_date <= end_date:
            try:
                result = use_case.execute(
                    product_code=product_code,
                    run_date=run_date,
                    force=force,
                    reason="test",
                    created_by="test_user",
                )
                print(result)
            except exceptions.ApplicationValidationError as exc:
                print(exc)

            run_date = run_date + timedelta(days=1)

        # rep_use_case = ReportStatsUseCase()
        # res = rep_use_case.execute(product_code, end_date)
        # from pprint import pprint

        # pprint(res.datapoints.to_dict())
        # assert 1 == 2

    @staticmethod
    def assert_expected(expected):
        rep_use_case = ReportStatsUseCase()
        for row in expected:

            def assertor(stats):
                stats_dict = stats.datapoints.to_dict()
                for k, v in row.items():
                    if isinstance(v, Decimal):
                        assert round(stats_dict[k], 12) == round(v, 12)
                    else:
                        assert stats_dict[k] == v

            run_date = row["price_date"]
            stats = rep_use_case.execute(
                product_code=row["product_code"], run_date=run_date
            )
            assertor(stats)


@pytest.fixture(scope="package")
def helpers():
    return Helpers

