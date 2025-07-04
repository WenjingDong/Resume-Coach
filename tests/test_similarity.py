import psycopg, os, numpy as np
from backend.scripts.embed_loader import embed
import pytest
pytestmark = pytest.mark.integration


def cosine(q, v):
    return np.dot(q, v)/(np.linalg.norm(q) * np.linalg.norm(v))

def test_similarity():
    db = psycopg.connect(os.environ["DATABASE_URL"])
    cur = db.cursor()

    q_vec = embed("machine learning engineers with PyTorch experience")

    cur.execute(
        "SELECT chunk, embedding FROM resume_chunks "
        "ORDER BY embedding <-> %s LIMIT 3",
        (q_vec, )
    )

    rows = cur.fetchall()
    assert any("PyTorch" in r[0] for r in rows)



