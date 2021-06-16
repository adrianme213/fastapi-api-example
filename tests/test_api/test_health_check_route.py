import fakeredis
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import get_fastapi_app


def test_health_check_successful(client: TestClient):
    res = client.get(f"/api/health")
    data = res.json()

    assert data
    assert res.status_code == 200


def test_health_check_failure():
    rc = fakeredis.FakeStrictRedis(decode_responses=True)

    def raise_503_error(app):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Error service unavailable.",
        )

    with patch.object(get_fastapi_app, '____', return_value=rc):
        with patch.object(get_fastapi_app, '____', new=raise_503_error):
            test_app = get_fastapi_app()
            with TestClient(test_app) as client:
                res = client.get(f"api/health")
                data = res.json()

                assert data["errors"]
                assert res.status_code == 503
