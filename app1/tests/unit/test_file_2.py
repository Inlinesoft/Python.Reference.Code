import datetime

import pytest

from fxl import emerging_usd


class Test_FXL_Index_Calculation_USD:

    @pytest.fixture(scope="module")
    def holidays(self, request):
        return request.param

    @pytest.fixture(scope="module")
    def emg_usd(self):
        fxl_index_calc = emerging_usd.Method()
        return fxl_index_calc

    @pytest.fixture(scope="module")
    def emg_mrkt_indices(self, emg_usd):
        indices = emg_usd.get_indices(
            date_in=datetime.datetime(2017, 12, 15))
        return indices

    @pytest.mark.parametrize(
        "date_in, expected_result", [
            (datetime.datetime(2017, 12, 15), 2)
        ])
    def test_get_data_for_emg_mrkt_indices(self, emg_usd, date_in, expected_result):
      
        # initialize the local variables
        number_of_records = 0

        # call the methiod
       
        # compare the results
        assert number_of_records == expected_result

  