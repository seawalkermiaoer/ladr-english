import os
import tempfile

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app import db


@pytest.fixture(autouse=True)
def temp_db(monkeypatch):
    fd, path = tempfile.mkstemp(prefix="words_test_", suffix=".db")
    os.close(fd)
    monkeypatch.setenv("WORD_DB_URL", f"sqlite:///{path}")
    db.override_database(os.environ["WORD_DB_URL"]) 
    try:
        yield
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


def client():
    return TestClient(app)


def test_health():
    c = client()
    r = c.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_create_and_get_word():
    c = client()
    payload = {"text": "hello", "definition": "greeting", "source": "test"}
    r = c.post("/api/words", json=payload)
    assert r.status_code == 200
    data = r.json()
    wid = data["id"]
    assert data["text"] == "hello"

    r2 = c.get(f"/api/words/{wid}")
    assert r2.status_code == 200
    assert r2.json()["text"] == "hello"


def test_list_and_search():
    c = client()
    for w in ["alpha", "beta", "alphabet"]:
        c.post("/api/words", json={"text": w})

    r = c.get("/api/words", params={"skip": 0, "limit": 10})
    assert r.status_code == 200
    assert r.json()["total"] >= 3

    r2 = c.get("/api/words", params={"q": "alpha"})
    assert r2.status_code == 200
    items = r2.json()["items"]
    assert any(i["text"] == "alpha" for i in items)
    assert any(i["text"] == "alphabet" for i in items)


def test_update_word_and_uniqueness():
    c = client()
    a = c.post("/api/words", json={"text": "one"}).json()
    b = c.post("/api/words", json={"text": "two"}).json()

    r = c.put(f"/api/words/{a['id']}", json={"text": "two"})
    assert r.status_code == 400

    r2 = c.put(f"/api/words/{b['id']}", json={"definition": "number"})
    assert r2.status_code == 200
    assert r2.json()["definition"] == "number"


def test_review_and_stats():
    c = client()
    w = c.post("/api/words", json={"text": "reviewme"}).json()

    r = c.post(f"/api/words/{w['id']}/review", json={"quality": 3})
    assert r.status_code == 200
    data = r.json()
    assert data["review_count"] == 1
    assert data["easiness"] >= 1.3
    assert data["due_date"] is not None

    stats = c.get("/api/stats").json()
    assert stats["total"] >= 1
    assert stats["reviewed"] >= 1


def test_delete_word():
    c = client()
    w = c.post("/api/words", json={"text": "bye"}).json()
    r = c.delete(f"/api/words/{w['id']}")
    assert r.status_code == 200
    r2 = c.get(f"/api/words/{w['id']}")
    assert r2.status_code == 404
