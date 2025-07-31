import psycopg, os, numpy as np
from backend.scripts.embed_loader import embed
import pytest
from conftest import insert_dummy_chunk

pytestmark = pytest.mark.integration


def cosine(q, v):
    return np.dot(q, v)/(np.linalg.norm(q) * np.linalg.norm(v))

def test_similarity():
    db = psycopg.connect(os.environ["DATABASE_URL"])
    cur = db.cursor()

    # Insert a chunk that proves PyTorcn skill
    insert_dummy_chunk(cur, "unit_test", "Implemented a DL application in PyTorch")
    db.commit()

    q_vec = embed("machine learning engineers with PyTorch experience")

    cur.execute(
        "SELECT chunk, embedding FROM resume_chunks "
        "ORDER BY embedding <-> %s::vector LIMIT 3",
        (q_vec, )
    )

    db.commit()
    rows = cur.fetchall()
    print(rows[0])
    assert any("PyTorch" in r[0] for r in rows)



