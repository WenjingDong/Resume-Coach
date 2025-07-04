import re, yaml, pathlib

PATTERNS = {
    s.lower(): re.compile(rf"\b{s}\b", re.I)
    for s in yaml.safe_load(pathlib.Path(__file__).with_name("skills.yaml").read_text())
}


def extract_skills(text: str) -> set[str]:
    return {k for k, pat in PATTERNS.items() if pat.search(text)}
