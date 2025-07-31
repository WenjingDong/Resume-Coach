# tests/conftest.py
import os, types, pytest, numpy as np, openai, psycopg


# 2 — mock psycopg.connect so tests never touch the DB
class _FakeCur(types.SimpleNamespace):
    execute = fetchone = fetchall = lambda *a, **k: None
    def __enter__(self): return self
    def __exit__(self, *exc): return False
class _FakeConn(types.SimpleNamespace):
    def cursor(self): return _FakeCur()
    def commit(self): pass
    def close(self):  pass
@pytest.fixture
def _mock_psycopg(monkeypatch):
    monkeypatch.setattr(psycopg, "connect", lambda *a, **k: _FakeConn())

# 3 — always set DATABASE_URL so import-time look-ups don’t KeyError
@pytest.fixture(autouse=True)
def _ensure_db_url(monkeypatch):
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql://resume:secret@localhost:6572/resumes?sslmode=disable"
    )
