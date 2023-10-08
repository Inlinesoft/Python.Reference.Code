import csv
from datetime import date, datetime
from decimal import Decimal

import inject

from app1.domain.entities import (
    Config,
)

from ..services.uow import UnitOfWork


def load_configs(uow: UnitOfWork):
    configs = [
        Config(
            namespace="product",
            config_code="BTCW",
            value={
                "initial_price_date": date(2019, 11, 27),
                "initial_asset_entitlement": Decimal("0.01"),
                "seed_end_date": date(2019, 11, 28),
                "annual_management_fee": Decimal("0.0095"),
                "asset_entitlement_rounding": "ROUND_HALF_UP",
                "capital_adjustment_factor": Decimal("0.0"),
                "index_ticker": "BRR",
            },
            as_of=datetime.strptime("2019-11-28", "%Y-%m-%d").date(),
            reason="test",
            created_by="test_user",
        ),
        Config(
            namespace="product",
            config_code="GBSP",
            value={
                "initial_price_date": date(2019, 12, 31),
                "initial_asset_entitlement": Decimal("0.007400903"),
                "annual_management_fee": Decimal("0.0039"),
                "annual_swap_fee": Decimal("0.0026"),
                "annual_subsidy_fee": Decimal("0.0014"),
                "index_ticker": "MSCEGLDG",
            },
            as_of=datetime.strptime("2019-11-28", "%Y-%m-%d").date(),
            reason="test",
            created_by="test_user",
        ),
        Config(
            namespace="product",
            config_code="GBSE",
            value={
                "initial_price_date": date(2019, 12, 31),
                "initial_asset_entitlement": Decimal("0.006955680"),
                "annual_management_fee": Decimal("0.0039"),
                "annual_swap_fee": Decimal("0.0016"),
                "annual_subsidy_fee": Decimal("0.0014"),
                "index_ticker": "MSCEGLDE",
            },
            as_of=datetime.strptime("2019-11-28", "%Y-%m-%d").date(),
            reason="test",
            created_by="test_user",
        ),
        Config(
            namespace="product",
            config_code="BULL",
            value={
                "microsecurities": [
                    {"product_code": "BULL", "microsecs": 1000000},
                ],
                "initial_multipliers": {"BULL": Decimal("0.9964668")},
                "initial_price_date": date(2019, 11, 29),
                "annual_management_fee": Decimal("0.0049"),
                "annual_licence_fee": Decimal("0.0005"),
                "annual_swap_fee": Decimal("0.0045"),
                "index_ticker": "BCOMGC",
            },
            as_of=datetime.strptime("2019-11-29", "%Y-%m-%d").date(),
            reason="test",
            created_by="test_user",
        ),
        Config(
            namespace="product",
            config_code="LALU",
            value={
                "initial_price_date": date(2019, 11, 29),
                "initial_price": Decimal("2.0650310"),
                "initial_is_market_disruption": False,
                "annual_management_fee": Decimal("0.0098"),
                "annual_licence_fee": Decimal("0.0005"),
                "annual_swap_fee": Decimal("0.0130"),
                "index_ticker": "BCOMAL",
            },
            as_of=datetime.strptime("2019-11-29", "%Y-%m-%d").date(),
            reason="test",
            created_by="test_user",
        ),
        Config(
            namespace="product",
            config_code="EBUL",
            value={
                "initial_price_date": date(2019, 11, 29),
                "initial_price": Decimal("6.5709292"),
                "initial_is_market_disruption": False,
                "annual_management_fee": Decimal("0.0049"),
                "annual_licence_fee": Decimal("0.0005"),
                "annual_swap_fee": Decimal("0.0067"),
                "index_ticker": "BUGCDE",
            },
            as_of=datetime.strptime("2019-11-29", "%Y-%m-%d").date(),
            reason="test",
            created_by="test_user",
        ),
        Config(
            namespace="product",
            config_code="EALL",
            value={
                "initial_price_date": date(2019, 11, 29),
                "initial_price": Decimal("4.5600613"),
                "initial_is_market_disruption": False,
                "annual_management_fee": Decimal("0.0049"),
                "annual_licence_fee": Decimal("0.0005"),
                "annual_swap_fee": Decimal("0.0067"),
                "index_ticker": "BCOMDE",
            },
            as_of=datetime.strptime("2019-11-29", "%Y-%m-%d").date(),
            reason="test",
            created_by="test_user",
        ),
        Config(
            namespace="product",
            config_code="SIME",
            value={
                "initial_price_date": date(2019, 11, 29),
                "initial_price": Decimal("45.9212735"),
                "initial_is_market_disruption": False,
                "annual_management_fee": Decimal("0.0098"),
                "annual_licence_fee": Decimal("0.0005"),
                "annual_swap_fee": Decimal("0.0085"),
                "index_ticker": "BCOMIN",
            },
            as_of=datetime.strptime("2019-11-29", "%Y-%m-%d").date(),
            reason="test",
            created_by="test_user",
        ),
        Config(
            namespace="product",
            config_code="SLVR",
            value={
                "microsecurities": [
                    {"product_code": "SLVR", "microsecs": 1000000},
                ],
                "initial_multipliers": {"SLVR": Decimal("0.9964668")},
                "initial_price_date": date(2019, 11, 29),
                "annual_management_fee": Decimal("0.0049"),
                "annual_licence_fee": Decimal("0.0005"),
                "annual_swap_fee": Decimal("0.0045"),
                "index_ticker": "BCOMSI",
            },
            as_of=datetime.strptime("2019-11-29", "%Y-%m-%d").date(),
            reason="test",
            created_by="test_user",
        ),
        Config(
            namespace="product",
            config_code="AIGP",
            value={
                "microsecurities": [
                    {"product_code": "BULL", "microsecs": 819405},
                    {"product_code": "SLVR", "microsecs": 255976},
                ],
                "initial_multipliers": {
                    "BULL": Decimal("0.9964668"),
                    "SLVR": Decimal("0.9964668"),
                },
                "initial_price_date": date(2019, 11, 29),
                "annual_management_fee": Decimal("0.0049"),
                "annual_licence_fee": Decimal("0.0005"),
                "annual_swap_fee": Decimal("0.0045"),
                "index_ticker": "BCOMPR",
            },
            as_of=datetime.strptime("2019-11-29", "%Y-%m-%d").date(),
            reason="test",
            created_by="test_user",
        ),
        Config(
            namespace="product",
            config_code="AIGP",
            value={
                "microsecurities": [
                    {"product_code": "BULL", "microsecs": 822573},
                    {"product_code": "SLVR", "microsecs": 252689},
                ],
                "initial_multipliers": {
                    "BULL": Decimal("0.9964668"),
                    "SLVR": Decimal("0.9964668"),
                },
                "initial_price_date": date(2019, 11, 29),
                "annual_management_fee": Decimal("0.0049"),
                "annual_licence_fee": Decimal("0.0005"),
                "annual_swap_fee": Decimal("0.0045"),
                "index_ticker": "BCOMPR",
            },
            as_of=datetime.strptime("2020-01-09", "%Y-%m-%d").date(),
            reason="test",
            created_by="test_user",
        ),
        Config(
            namespace="product",
            config_code="AIGP",
            value={
                "microsecurities": [
                    {"product_code": "BULL", "microsecs": 825713},
                    {"product_code": "SLVR", "microsecs": 249402},
                ],
                "initial_multipliers": {
                    "BULL": Decimal("0.9964668"),
                    "SLVR": Decimal("0.9964668"),
                },
                "initial_price_date": date(2019, 11, 29),
                "annual_management_fee": Decimal("0.0049"),
                "annual_licence_fee": Decimal("0.0005"),
                "annual_swap_fee": Decimal("0.0045"),
                "index_ticker": "BCOMPR",
            },
            as_of=datetime.strptime("2020-01-10", "%Y-%m-%d").date(),
            reason="test",
            created_by="test_user",
        ),
        Config(
            namespace="product",
            config_code="AIGP",
            value={
                "microsecurities": [
                    {"product_code": "BULL", "microsecs": 828871},
                    {"product_code": "SLVR", "microsecs": 246115},
                ],
                "initial_multipliers": {
                    "BULL": Decimal("0.9964668"),
                    "SLVR": Decimal("0.9964668"),
                },
                "initial_price_date": date(2019, 11, 29),
                "annual_management_fee": Decimal("0.0049"),
                "annual_licence_fee": Decimal("0.0005"),
                "annual_swap_fee": Decimal("0.0045"),
                "index_ticker": "BCOMPR",
            },
            as_of=datetime.strptime("2020-01-13", "%Y-%m-%d").date(),
            reason="test",
            created_by="test_user",
        ),
        Config(
            namespace="product",
            config_code="AIGP",
            value={
                "microsecurities": [
                    {"product_code": "BULL", "microsecs": 832029},
                    {"product_code": "SLVR", "microsecs": 242828},
                ],
                "initial_multipliers": {
                    "BULL": Decimal("0.9964668"),
                    "SLVR": Decimal("0.9964668"),
                },
                "initial_price_date": date(2019, 11, 29),
                "annual_management_fee": Decimal("0.0049"),
                "annual_licence_fee": Decimal("0.0005"),
                "annual_swap_fee": Decimal("0.0045"),
                "index_ticker": "BCOMPR",
            },
            as_of=datetime.strptime("2020-01-14", "%Y-%m-%d").date(),
            reason="test",
            created_by="test_user",
        ),
        Config(
            namespace="product",
            config_code="AIGP",
            value={
                "microsecurities": [
                    {"product_code": "BULL", "microsecs": 835155},
                    {"product_code": "SLVR", "microsecs": 239541},
                ],
                "initial_multipliers": {
                    "BULL": Decimal("0.9964668"),
                    "SLVR": Decimal("0.9964668"),
                },
                "initial_price_date": date(2019, 11, 29),
                "annual_management_fee": Decimal("0.0049"),
                "annual_licence_fee": Decimal("0.0005"),
                "annual_swap_fee": Decimal("0.0045"),
                "index_ticker": "BCOMPR",
            },
            as_of=datetime.strptime("2020-01-15", "%Y-%m-%d").date(),
            reason="test",
            created_by="test_user",
        ),
        Config(
            namespace="issuer",
            config_code="WIXL",
            value={
                "email": {
                    "enabled": True,
                    "to": [],
                    "cc": [],
                    "bcc": [],
                },
                "ftp": {
                    "enabled": True,
                },
                "cdb_publish": {
                    "enabled": True,
                },
            },
            as_of=datetime.strptime("2020-01-01", "%Y-%m-%d").date(),
            reason="test",
            created_by="test_user",
        ),
        Config(
            namespace="issuer",
            config_code="WIRX001",
            value={
                "email": {
                    "enabled": False,
                    "to": [],
                    "cc": [],
                    "bcc": [],
                },
                "ftp": {
                    "enabled": False,
                },
                "cdb_publish": {
                    "enabled": False,
                },
            },
            as_of=datetime.strptime("2020-01-01", "%Y-%m-%d").date(),
            reason="test",
            created_by="test_user",
        ),
        Config(
            namespace="product",
            config_code="PHPT.PCOM",
            value={
                "initial_price_date": date(2021, 6, 1),
                "initial_metal_entitlement": Decimal("0.093306538"),
                "annual_management_fee": Decimal("0.0049000"),
                "index_ticker": "XPTUSD F130 Curncy",
            },
            as_of=datetime.strptime("2019-11-28", "%Y-%m-%d").date(),
            reason="test",
            created_by="test_user",
        ),
        Config(
            namespace="product",
            config_code="PHPM",
            value={
                "initial_price_date": date(2021, 6, 1),
                "securities": [
                    # ticker links to product in order to get index
                    # and annual_management_fee1
                    {"ticker": "PHAU", "weight": Decimal(0.4000000)},
                    {"ticker": "PHAG", "weight": Decimal(1.2000000)},
                    {"ticker": "PHPT", "weight": Decimal(0.1000000)},
                    {"ticker": "PHPD", "weight": Decimal(0.2000000)},
                ],
                "annual_management_fee": Decimal(
                    "0.004400"
                ),  # TODO: not used?
                "index_ticker": "1676 JP",
            },
            as_of=datetime.strptime("2019-11-28", "%Y-%m-%d").date(),
            reason="test",
            created_by="test_user",
        ),
        Config(
            namespace="issuer",
            config_code="MSL",
            value={
                "email": {
                    "enabled": False,
                    "to": [],
                    "cc": [],
                    "bcc": [],
                },
                "ftp": {
                    "enabled": False,
                },
                "cdb_publish": {
                    "enabled": False,
                },
            },
            as_of=datetime.strptime("2020-01-01", "%Y-%m-%d").date(),
            reason="test",
            created_by="test_user",
        ),
        Config(
            namespace="product",
            config_code="PHPD",
            value={
                "initial_price_date": date(2021, 6, 1),
                "initial_metal_entitlement": "0.093306538000000",
                "annual_management_fee": "0.00490000000",
                "index_ticker": "PLDMLNPM Index",
            },
            as_of=datetime.strptime("2019-11-28", "%Y-%m-%d").date(),
            reason="test",
            created_by="test_user",
        ),
        Config(
            namespace="product",
            config_code="PHAU",
            value={
                "initial_price_date": date(2021, 6, 1),
                "initial_metal_entitlement": "0.094637774000000",
                "annual_management_fee": "0.00390000000",
                "index_ticker": "GOLDLNPM Index",
            },
            as_of=datetime.strptime("2019-11-28", "%Y-%m-%d").date(),
            reason="test",
            created_by="test_user",
        ),
        Config(
            namespace="product",
            config_code="PHAG",
            value={
                "initial_price_date": date(2021, 6, 1),
                "initial_metal_entitlement": "0.933065373000000",
                "annual_management_fee": "0.00490000000",
                "index_ticker": "SLVRLND Index",
            },
            as_of=datetime.strptime("2019-11-28", "%Y-%m-%d").date(),
            reason="test",
            created_by="test_user",
        ),
        Config(
            namespace="product",
            config_code="PHPT",
            value={
                "initial_price_date": date(2021, 6, 1),
                "initial_metal_entitlement": "0.093306538000000",
                "annual_management_fee": "0.00490000000",
                "index_ticker": "PLTMLNPM Index",
            },
            as_of=datetime.strptime("2019-11-28", "%Y-%m-%d").date(),
            reason="test",
            created_by="test_user",
        ),
        Config(
            namespace="product",
            config_code="SGBS",
            value={
                "initial_price_date": date(2021, 6, 1),
                "initial_metal_entitlement": "0.096317001000000",
                "annual_management_fee": "0.00150000000",
                "index_ticker": "GOLDLNPM Index",
            },
            as_of=datetime.strptime("2019-11-28", "%Y-%m-%d").date(),
            reason="test",
            created_by="test_user",
        ),
        Config(
            namespace="product",
            config_code="WGLD",
            value={
                "initial_price_date": date(2021, 6, 1),
                "initial_metal_entitlement": "0.099926048000000",
                "annual_management_fee": "0.00150000000",
                "index_ticker": "GOLDLNPM Index",
            },
            as_of=datetime.strptime("2019-11-28", "%Y-%m-%d").date(),
            reason="test",
            created_by="test_user",
        ),
    ]
    uow.configs_repo.save(configs)
