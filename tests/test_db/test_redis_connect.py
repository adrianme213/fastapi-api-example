import pytest
from rediscluster.exceptions import RedisClusterException
from app.db.redis_connect import redis_connect
from app.core.config import config_name_str

conf = config_name_str()
TEST_DEV_REDIS_HOST = conf["REDIS"]["HOST"]


@pytest.mark.slow
def test_redis_connect():
    """Check redis connection to cluster."""
    redis_host = TEST_DEV_REDIS_HOST
    redis_username = "default"
    redis_password = ""
    rc = redis_connect(host=redis_host, username=redis_username, password=redis_password)
    response = rc.ping()
    assert response is not None


@pytest.mark.slow
def test_redis_connect_fail():
    """Check redis connection fails to connect to cluster."""
    redis_host = TEST_DEV_REDIS_HOST
    redis_username = "bad_username"
    redis_password = "not_a_password"
    with pytest.raises(RedisClusterException) as excinfo:
        rc = redis_connect(host=redis_host, username=redis_username, password=redis_password)

    assert str(excinfo.value) is not None
