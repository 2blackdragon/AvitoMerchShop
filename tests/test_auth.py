import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_success():
    response = client.post("/auth/token", data={"username": "testuser", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_credentials():
    response = client.post("/auth/token", data={"username": "invaliduser", "password": "wrongpassword"})
    assert response.status_code == 400
    assert "Invalid credentials" in response.json()["detail"]
