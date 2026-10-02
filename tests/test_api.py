from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_health_check():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == "healthy"

def test_create_short_url():

    response = client.post(

        "/urls",

        json={

            "original_url": "https://example.com"

        },

    )

    assert response.status_code == 201

    data = response.json()

    assert data["original_url"] == "https://example.com"

    assert data["short_code"]

def test_missing_short_url_returns_404():

    response = client.get("/does-not-exist")

    assert response.status_code == 404
