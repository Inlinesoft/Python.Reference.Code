import os

import inject
import pytest
from fastapi.testclient import TestClient

from infrastructure.entrypoints.api.main import app
from infrastructure.services.db import setup_and_load_db_repos


@pytest.fixture(
    scope="session",
    autouse=True,
    params=[setup_and_load_db_repos],
)
def setup_data_repos(request):
    request.param()
    yield True
    inject.clear()


@pytest.fixture(scope="session")
def test_api_client():
    client = TestClient(app)  # todo: http://api.com ??
    api_user = os.environ["API_USERNAME"].split(",")[0]
    api_pwd = os.environ["API_PASSWORD"].split(",")[0]
    client.auth = (api_user, api_pwd)
    return client