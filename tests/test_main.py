from fastapi.testclient import TestClient

from main import app


def test_read_root():
    response = TestClient(app).get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}
