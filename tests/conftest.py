import os
import tempfile
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from app.main import app

@pytest.fixture
def client(monkeypatch):
    with tempfile.TemporaryDirectory() as folder:
        monkeypatch.setenv("DB_PATH", str(Path(folder) / "test.db"))
        with TestClient(app) as c:
            yield c

@pytest.fixture
def login_as(client):
    def login(email, password):
        resp = client.post("/api/auth/login", json={"email": email, "password": password})
        assert resp.status_code == 200, resp.text
        return {"Authorization": f"Bearer {resp.json()['access_token']}"}
    return login
