from fastapi import FastAPI
from fastapi import HTTPException, status, UploadFile, File, Body
from backend.parsers.pdf_parser import parse_pdf
import logging, sys
from backend.scripts.embed_loader import embed
from backend.analysis.scorer import score_resume
from pydantic import BaseModel

class AnalyzeReq(BaseModel):
    resume_id: str
    jd_text: str


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
app = FastAPI()

@app.get("/healthz")

def health():
    return {"status": "ok"}

@app.post("/parse-resume")
async def parse_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF resumes are accepted.",
        )
    content = await file.read()
    return parse_pdf(content)

@app.post("/search")
async def search(query: str = Body(embed=True)):
    vec = embed(query)
    cur = app.state.db.cursor()
    cur.execute(
        "SELECT resume_id, chunk "
        "FROM resume_chunks ORDER BY embedding <-> %s LIMIT 5",
        (vec,)
    )
    return [{"resume_id": r[0], "snippet": r[1]} for r in cur.fetchall()]

@app.post("/analyze")
def analyze(req: AnalyzeReq):
    return score_resume(req.resume_id, req.jd_text)