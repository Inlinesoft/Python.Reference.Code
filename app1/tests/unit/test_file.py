import datetime
import pytest
import os

#from config.definitions import *
from config import definitions
from . import fee_calculation


class Test_FXL_Fee_Calculation():

    @pytest.fixture(scope="module")
    def emerging_mrkt_date(self, request):
        yield request.param

    @pytest.fixture(scope="module")
    def fxl_products(self, fee_calculation):
        return fee_calculation.get_products_data(product_issuer_id=2)

    @pytest.mark.parametrize(
        "issuer_id,selected_products, expected_result", [
            (2, [], 58)
            , (2, [1974, 1979, 1980], 3)
            , (1, [], 0)
        ])
    def test_get_products_data(self, fee_calculation, product_issuer_id, selected_products, expected_result):
        """

      
        """
        # initialize the local variables
        number_of_records = 0

        # call the methiod
        df_products = fee_calculation.get_products_data(product_issuer_id=product_issuer_id,
                                                            selected_products=selected_products)

        # get the results
        if (df_products):
            number_of_records = len(df_products)

        # compare the results

        assert number_of_records == expected_result