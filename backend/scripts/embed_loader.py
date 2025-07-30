import os, json, textwrap
from pathlib import Path
import openai, psycopg
from backend.parsers.pdf_parser import parse_pdf
from sentence_transformers import SentenceTransformer
import requests

# Load once at module level
model = SentenceTransformer("all-mpnet-base-v2")  # You can swap in other models later

def embed(text: str) -> list[float]:
    return model.encode(text).tolist()


# openai.api_key = os.environ['OPENAI_API_KEY']
conn = None
CHUNK_TOKENS = 400  # keep under model limit


def get_conn():
    global conn
    if conn is None:
        conn = psycopg.connect(os.getenv("DATABASE_URL", "postgresql://resume:secret@localhost:5433/resumes"))
    return conn


def embed(text: str):
    return model.encode(text).tolist()


def load_resume(pdf_path: Path):
    parsed = parse_pdf(pdf_path)
    raw = parsed["metadata"]["text_only"]
    # simple chunking: wrap every N tokesn into ~CHUNK_TOKENS-sized pieces
    get_conn()
    cur = conn.cursor()

    for idx, chunk in enumerate(textwrap.wrap(raw, 3500)):  # 3500 chars ~ 400 tokens
        cur.execute(
            """
            INSERT INTO resume_chunks (resume_id, chunk, embedding)
            VALUES (%s, %s, %s)
            """,
            (pdf_path.stem, chunk, embed(chunk))
        )
    conn.commit()


def store_resume_chunks(resume_id: str, resume_text: str):
    chunks = textwrap.wrap(resume_text, 3500)  # ≈400 tokens each
    get_conn()
    cur = conn.cursor()

    for chunk in chunks:
        vec = embed(chunk)  # Embed with OpenAI or other model
        vec_str = f"[{', '.join(map(str, vec))}]"
        cur.execute(
            "INSERT INTO resume_chunks (resume_id, chunk, embedding) VALUES (%s, %s, %s::vector)",
            (resume_id, chunk, vec_str)
        )

    conn.commit()
    conn.close()


def call_local_llm(prompt: str, model: str = "mistral") -> str:
    try:
        res = requests.post("http://localhost:11434/api/generate", json={
            "model": model,
            "prompt": prompt,
            "stream": False
        })
        return res.json()["response"].strip()
    except Exception as e:
        return f"(LLM Error: {e})"


if __name__ == "__main__":
    for pdf in Path("samples").glob("*.pdf"):
        load_resume(pdf)
    print("embeddings loaded")