from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_recommend_endpoint():
    resume_text = (
        "Experienced ML engineer with Python, PyTorch, and FastAPI experience. "
        "Also worked on deployment with Docker and Kubernetes."
    )

    response = client.post("/recommend", json={"resume_text": resume_text})
    assert response.status_code == 200

    data = response.json()

    # Check extracted skills
    assert isinstance(data["skills"], list)
    assert "python" in data["skills"] or "pytorch" in data["skills"]

    # Check recommendation structure
    recommendations = data["recommendations"]
    assert isinstance(recommendations, list)
    assert len(recommendations) > 0

    first = recommendations[0]
    assert "job_id" in first
    assert "score" in first
    assert "matched_skills" in first
    assert isinstance(first["matched_skills"], list)
