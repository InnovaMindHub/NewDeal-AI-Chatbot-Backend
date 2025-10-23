import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    # Accepter 'healthy' ou 'degraded' comme statuts valides
    status = response.json()["status"]
    assert status in ["healthy", "degraded"], f"Status attendu: healthy ou degraded, reçu: {status}"