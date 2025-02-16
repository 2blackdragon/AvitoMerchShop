import pytest


def test_login_success(client):
    response = client.post("/api/auth", data={"username": "testuser", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_credentials(client):
    response = client.post("/api/auth", data={"username": "testuser", "password": "password"})
    assert response.status_code == 200
    response = client.post("/api/auth", data={"username": "testuser", "password": "wrongpassword"})
    assert response.status_code == 400
    assert "Incorrect username or password" in response.json()["detail"]
