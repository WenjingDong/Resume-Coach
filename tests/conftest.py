# tests/conftest.py
"""
Global test fixtures:
– mock_openai_embeddings  → returns a fixed 1 536-d vector
– mock_psycopg_connect    → provides a no-op connection / cursor
Both run automatically for every test (autouse=True).
"""

import os
import types
import pytest
import numpy as np
import openai
import psycopg


# --------------------------------------------------------------------------- #
# 1 -- Mock OpenAI embeddings so unit tests never hit the real API
# --------------------------------------------------------------------------- #
@pytest.fixture(autouse=True)
def mock_openai_embeddings(monkeypatch):
    """Monkey-patch openai.embeddings.create → constant unit vector."""
    def _fake_create(model, input):
        vec = np.zeros(1536, dtype=float)
        vec[0] = 1.0  # non-zero to avoid divide-by-zero in cosine
        return openai.types.EmbeddingList(
            data=[openai.types.Embedding(embedding=vec.tolist(), index=0)],
            model=model,
            object="list",
            usage=None,
        )

    monkeypatch.setattr(openai.embeddings, "create", _fake_create)


# --------------------------------------------------------------------------- #
# 2 -- Mock psycopg.connect so imports don’t need a live Postgres socket
# --------------------------------------------------------------------------- #
class _FakeCursor(types.SimpleNamespace):
    execute = fetchone = fetchall = lambda *a, **k: None
    def __enter__(self):             # allow “with conn.cursor() as cur:”
        return self
    def __exit__(self, *exc):        # no commit/rollback needed
        return False

class _FakeConn(types.SimpleNamespace):
    def cursor(self):                # psycopg.connect().cursor()
        return _FakeCursor()
    def commit(self):                # safe no-ops
        pass
    def close(self):
        pass

@pytest.fixture(autouse=True)
def mock_psycopg_connect(monkeypatch):
    """Replace psycopg.connect with a stub that returns _FakeConn()."""
    monkeypatch.setattr(psycopg, "connect", lambda *_, **__: _FakeConn())


# --------------------------------------------------------------------------- #
# 3 -- Ensure DATABASE_URL always exists (some code reads it at import-time)
# --------------------------------------------------------------------------- #
@pytest.fixture(autouse=True)
def ensure_database_url(monkeypatch):
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql://resume:secret@db/resumes?sslmode=disable",
    )
