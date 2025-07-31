# tests/conftest.py
import os, types, pytest, numpy as np, openai, psycopg
from backend.scripts.embed_loader import embed
def insert_dummy_chunk(cur, resume_id, text, vec=None):
    if vec is None:
        # vec = np.zeros(1536).tolist()
        # vec[0] = 1.0
        vec = embed(text)
    cur.execute(
        "INSERT INTO resume_chunks (resume_id, chunk, embedding)"
        "Values (%s, %s, %s)",
        (resume_id, text, vec)
    )

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
