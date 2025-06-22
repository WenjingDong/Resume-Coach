from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_reject_non_pdf():
    r = client.post(
        "/parse-resume",
        files={"file": ("foo.txt", b"hello", "text/plain")},
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "Only PDF resumes are accepted."
