import pandas

#from config.definitions import *
from config import definitions
import os


FIXTURE_DIR = os.path.join(definitions.common['ROOT_DIR'], 'test_files', 'unit_tests')


def pytest_generate_tests(metafunc):

    if 'index_historical_values' in metafunc.fixturenames:
        df_data = index.get_index_historical_values()
        metafunc.parametrize("index_historical_values", [df_data])

    if 'emerging_mrkt_date' in metafunc.fixturenames:
        df_dates = pandas.read_csv(os.path.join(FIXTURE_DIR, 'emerging_mrkt_dates.csv'))
        # df_dates = df_dates[df_dates['index_id'] == 856]
        metafunc.parametrize("emerging_mrkt_date",
                             df_dates.to_dict(orient="records"),
                             indirect=True)
