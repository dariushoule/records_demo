from fastapi.testclient import TestClient

from records import app

client = TestClient(app)


def test_read_records_empty():
    response = client.get("/records")
    assert response.status_code == 200
    assert response.json() == []