# tests/conftest.py
import os, types, pytest, numpy as np, openai, psycopg

# 1 — mock OpenAI embeddings (avoids real network & new client kwargs)
class _DummyEmbeddings(types.SimpleNamespace):
    def create(self, model, input):
        vec = np.zeros(1536); vec[0] = 1.0
        return openai.types.EmbeddingList(
            data=[openai.types.Embedding(embedding=vec.tolist(), index=0)],
            model=model, object="list", usage=None,
        )
@pytest.fixture(autouse=True)
def _patch_openai(monkeypatch):
    monkeypatch.setattr(openai, "embeddings", _DummyEmbeddings(), raising=False)

# 2 — mock psycopg.connect so tests never touch the DB
class _FakeCur(types.SimpleNamespace):
    execute = fetchone = fetchall = lambda *a, **k: None
    def __enter__(self): return self
    def __exit__(self, *exc): return False
class _FakeConn(types.SimpleNamespace):
    def cursor(self): return _FakeCur()
    def commit(self): pass
    def close(self):  pass
@pytest.fixture(autouse=True)
def _mock_psycopg(monkeypatch):
    monkeypatch.setattr(psycopg, "connect", lambda *a, **k: _FakeConn())

# 3 — always set DATABASE_URL so import-time look-ups don’t KeyError
@pytest.fixture(autouse=True)
def _ensure_db_url(monkeypatch):
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql://resume:secret@localhost:6572/resumes?sslmode=disable"
    )
