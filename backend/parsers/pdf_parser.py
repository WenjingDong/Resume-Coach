import io
from pathlib import Path
import pdfplumber
from typing import Dict, List, Any

def parse_pdf(path_or_bytes) -> Dict[str, Any]:
    """ Return JSON dict conforming to docs/parse-schema.md."""
    if isinstance(path_or_bytes, (str, Path)):
        pdf_file = open(path_or_bytes, "rb")
    else:
        pdf_file = io.BytesIO(path_or_bytes)

    pages: List[dict] = []
    full_text = []

    with pdfplumber.open(pdf_file) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            lines = [
                {"text": obj["text"], "x0": obj["x0"], "top": obj["top"]}
                for obj in page.extract_words(x_tolerance=1, y_tolerance=3)
            ]
            pages.append({"pages_num": i, "lines": lines})
            full_text.append(page.extract_text() or "")

    return {"pages": pages, "metadata": {"text_only": "\n".join(full_text)}}

