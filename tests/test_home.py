# from datetime import datetime

from starlette.testclient import TestClient

from src.server import app

client = TestClient(app)


def test_request_sem_token():
    response = client.get('/')
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}
