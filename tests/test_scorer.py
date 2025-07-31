import os, psycopg, numpy as np
from backend.analysis.scorer import score_resume
from backend.analysis.skill_extractor import extract_skills
from backend.scripts.embed_loader import embed
from conftest import insert_dummy_chunk

import pytest
pytestmark = pytest.mark.integration



def test_score_resume(tmp_path):
    db = psycopg.connect(os.environ["DATABASE_URL"])
    cur = db.cursor()

    # Clean slate for this test
    cur.execute("DELETE FROM resume_chunks WHERE resume_id = 'unit_test'")
    db.commit()

    # Insert a chunk that proves Python skill
    insert_dummy_chunk(cur, "unit_test", "Build REST services in Python")
    db.commit()

    jd_text = "Looking for a backend engineer with strong Python skills."
    result = score_resume("unit_test", jd_text)

    assert result["score"] == 100
    assert "python" in result["matched"]
    assert result["missing"] == []