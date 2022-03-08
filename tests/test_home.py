from datetime import datetime

from starlette.testclient import TestClient

from src.server import app

client = TestClient(app)


def test_status_code():
    response = client.get('/')
    horario = datetime.now().strftime('%H:%M:%S')
    assert response.status_code == 200
    assert response.json() == {'msg': horario}
