from datetime import date
from decimal import Decimal

import pytest

from application.use_cases import ReportStatsUseCase


@pytest.fixture(scope="module")
def ebul(helpers):
    product_code = "EBUL"
    helpers.run_pricing(
        date(2019, 12, 2), date(2020, 3, 31), product_code, True
    )
    return product_code


def test_hcsl_ebul_nav_noraml_day(ebul):
    rep_use_case = ReportStatsUseCase()
    data = rep_use_case.execute(ebul, date(2019, 12, 2))
    result = data.datapoints.to_dict()
    assert result["capital_adjustment"] == Decimal("-0.00005110000000")
    assert result["nav"] == Decimal("6.5550405")
    assert result["creation_redemption_price"] == Decimal("6.5550405")