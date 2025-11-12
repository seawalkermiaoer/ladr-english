import os

import pytest
from fastapi.testclient import TestClient

from app.main import app


def client():
    return TestClient(app)


def test_missing_authorization_header():
    c = client()
    r = c.get("/api/verify")
    assert r.status_code == 401
    assert "Authorization" in r.json()["detail"] or r.json()["detail"] == "missing Authorization header"


def test_bearer_token_ok_without_secret():
    if "WORD_TOKEN_SECRET" in os.environ:
        del os.environ["WORD_TOKEN_SECRET"]
    c = client()
    r = c.get("/api/verify", headers={"Authorization": "Bearer abc123"})
    assert r.status_code == 200
    assert r.json()["ok"] is True
    assert r.json()["token"] == "abc123"


def test_bearer_token_must_match_secret(monkeypatch):
    monkeypatch.setenv("WORD_TOKEN_SECRET", "secret-token")
    c = client()
    r = c.get("/api/verify", headers={"Authorization": "Bearer wrong"})
    assert r.status_code == 401
    r2 = c.get("/api/verify", headers={"Authorization": "Bearer secret-token"})
    assert r2.status_code == 200
    assert r2.json()["token"] == "secret-token"

