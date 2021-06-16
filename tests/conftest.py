import pytest
import json
import fakeredis
from unittest.mock import patch
from fastapi.testclient import TestClient
from starlette.config import environ

environ['APP_ENV'] = 'dev'

from app.main import get_fastapi_app


@pytest.fixture(scope='module')
def client():
    rc = fakeredis.FakeStrictRedis(decode_responses=True)
    data1 = {}
    rc.hset('key', '1', json.dumps(data1))

    with patch.object(get_fastapi_app, '_redis_connect', return_value=rc):
        test_app = get_fastapi_app()
        with TestClient(test_app) as client:
            yield client


# Slow Test Tag Option
def pytest_addoption(parser):
    parser.addoption(
        "--slow", action="store_true", default=False, help="Run slow tests that require internet connection."
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--slow"):
        # --slow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="Need --slow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
