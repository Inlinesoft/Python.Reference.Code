from decimal import Decimal

import pytest

from domain.calculations import common


@pytest.mark.parametrize(
    "params,expected",
    [
        # positives
        ((Decimal("0.45678"), 4), Decimal("0.4568")),
        ((Decimal("0.45675"), 4), Decimal("0.4568")),
        ((Decimal("0.45674"), 4), Decimal("0.4567")),
        ((Decimal("0.4"), 0), Decimal("0")),
        ((Decimal("0.5"), 0), Decimal("1")),
        ((Decimal("0.5"), -1), Decimal("1")),
        ((Decimal("0.5"), -5), Decimal("1")),
        # negatives
        ((Decimal("-0.45678"), 4), Decimal("-0.4568")),
        ((Decimal("-0.45675"), 4), Decimal("-0.4568")),
        ((Decimal("-0.45674"), 4), Decimal("-0.4567")),
        ((Decimal("-0.4"), 0), Decimal("0")),
        ((Decimal("-0.5"), 0), Decimal("-1")),
        ((Decimal("-0.5"), -1), Decimal("-1")),
        ((Decimal("-0.5"), -5), Decimal("-1")),
    ],
)
def test_round_half_up(params, expected):
    actual = common.round_half_up(*params)
    assert actual == expected


@pytest.mark.parametrize(
    "params,expected",
    [
        # positives
        ((Decimal("0.45678"), 4), Decimal("0.4567")),
        ((Decimal("0.45675"), 4), Decimal("0.4567")),
        ((Decimal("0.45674"), 4), Decimal("0.4567")),
        ((Decimal("0.4"), 0), Decimal("0")),
        ((Decimal("0.5"), 0), Decimal("0")),
        ((Decimal("0.5"), -1), Decimal("0")),
        ((Decimal("0.5"), -5), Decimal("0")),
        # negatives
        ((Decimal("-0.45678"), 4), Decimal("-0.4567")),
        ((Decimal("-0.45675"), 4), Decimal("-0.4567")),
        ((Decimal("-0.45674"), 4), Decimal("-0.4567")),
        ((Decimal("-0.4"), 0), Decimal("0")),
        ((Decimal("-0.5"), 0), Decimal("0")),
        ((Decimal("-0.5"), -1), Decimal("0")),
        ((Decimal("-0.5"), -5), Decimal("0")),
    ],
)
def test_round_down(params, expected):
    actual = common.round_down(*params)
    assert actual == expected
