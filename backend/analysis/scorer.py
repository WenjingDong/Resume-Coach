import numpy as np, psycopg, os
from backend.analysis.skill_extractor import extract_skills
from backend.scripts.embed_loader import embed

THRESHOLD = 0.28 # Modify later


def cosine(a, b):
    return np.dot(a, b)/np.linalg.norm(a)/np.linalg.norm(b)


def score_resume(resume_id: str, jd_text: str, top_k=3) -> dict:
    skills = extract_skills(jd_text)
    db = psycopg.connect(os.environ["DATABASE_URL"])
    cur = db.cursor()

    matched, missing, detail = [], [], []

    for skill in skills:
        q_vec = embed(skill)
        cur.execute(
            "SELECT chunk, embedding FROM resume_chunks "
            "WHERE resume_id=%s ORDER BY embedding <-> %s LIMIT %s",
            (resume_id, q_vec, top_k)
        )
        rows = cur.fetchall()
        best = rows[0] if rows else None
        if best and cosine(q_vec, best[1]) >= THRESHOLD:
            matched.append(skill)
            detail.append({"skill": skill, "gap": False, "resume_snippet": best[0]})
        else:
            missing.append(skill)
            detail.append({"skill": skill, "gap": True, "jd_snippet": f"JD mentions {skill}"})

    score = int(len(matched) / max(len(skills), 1) * 100)
    return {"score": score, "matched": matched, "missing": missing,  "detail": detail}
