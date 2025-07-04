import os, json, textwrap
from pathlib import Path
import openai, psycopg
from backend.parsers.pdf_parser import parse_pdf

# openai.api_key = os.environ['OPENAI_API_KEY']
conn = None

CHUNK_TOKENS = 400 # keep under model limit

def get_conn():
    global conn
    if conn is None:
        conn = psycopg.connect(os.getenv("DATABASE_URL", "postgresql://resume:secret@localhost:5432/resumes"))
    return conn

def embed(text: str):
    if not openai.api_key:
        openai.api_key = os.getenv('OPENAI_API_KEY', "dummy")
    r = openai.embeddings.create(
        model="text-embedding-3-small", input=text
    )
    return r.data[0].embedding

def load_resume(pdf_path: Path):
    parsed = parse_pdf(pdf_path)
    raw = parsed["metadata"]["text_only"]
    # simple chunking: wrap every N tokesn into ~CHUNK_TOKENS-sized pieces
    get_conn()
    cur = conn.cursor()

    for idx, chunk in enumerate(textwrap.wrap(raw, 3500)): # 3500 chars ~ 400 tokens
        cur.execute(
            """
            INSERT INTO resume_chunks (resume_id, chunk, embedding)
            VALUES (%s, %s, %s)
            """,
            (pdf_path.stem, chunk, embed(chunk))
        )
    conn.commit()

if __name__ == "__main__":
    for pdf in Path("samples").glob("*.pdf"):
        load_resume(pdf)
    print("embeddings loaded")