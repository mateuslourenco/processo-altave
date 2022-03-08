from starlette.testclient import TestClient

from src.server import app

client = TestClient(app)


def test_status_code():
    response = client.get('/')
    assert response.status_code == 200
