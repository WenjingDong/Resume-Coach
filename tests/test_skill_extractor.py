from backend.analysis.skill_extractor import extract_skills


def test_extract_known_skills():
    text = "Expert in Python and kubernetes; familiar with CI/CD pipelines."
    skills = extract_skills(text)
    assert "python" in skills
    assert "kubernetes" in skills
    assert "ci/cd" in skills
