from backend.parsers.pdf_parser import parse_pdf
from pathlib import Path

def test_parse_sample_resume():
    data = parse_pdf(Path("samples/sample_resume.pdf"))
    assert "pages" in data and len(data["pages"]) >= 1
    # crude smoke checks
    first_page = data["pages"][0]
    assert first_page["page_num"] == 1
    assert any("Freshman" in l["text"] for l in first_page["lines"])
    assert "Email" in data["metadata"]["text_only"]
    assert len(first_page["lines"]) > 10
