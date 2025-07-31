from fastapi import FastAPI
from fastapi import HTTPException, status, UploadFile, File, Body
from backend.parsers.pdf_parser import parse_pdf
from backend.scripts.embed_loader import store_resume_chunks, call_local_llm
import logging,sys
from backend.scripts.embed_loader import embed
from backend.analysis.scorer import score_resume, match_score
from backend.analysis.skill_extractor import extract_skills
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from uuid import uuid4
import openai, os, json
import psycopg
from typing import List

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
JOBS_PATH = os.path.join(CURRENT_DIR,  "data", "sample_jobs.json")

class RecommendRequest(BaseModel):
    resume_text: str # or pass resumes and extract sills

class JobRecommendation(BaseModel):
    job_id: str
    title: str
    score: int
    matched_skills: List[str]

class RecommendationResponse(BaseModel):
    skills: List[str]
    recommendations: List[JobRecommendation]

class AnalyzeReq(BaseModel):
    resume_id: str
    jd_text: str


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    app.state.db = psycopg.connect(os.getenv("DATABASE_URL",  "postgresql://resume:secret@localhost:5433/resumes"))


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

@app.post("/upload")
async def upload(
        resume: UploadFile = File(...),
        job_description: UploadFile = File(...)
):
    if resume.content_type != "application/pdf" or job_description.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    resume_bytes = await resume.read()
    jd_bytes = await job_description.read()

    parsed = parse_pdf(resume_bytes)
    resume_text = parsed["metadata"]["text_only"]

    parsed = parse_pdf(jd_bytes)
    jd_text = parsed["metadata"]["text_only"]

    # Generate unique ID and store parsed resume
    resume_id = str(uuid4())

    #  Store embeddings into database
    store_resume_chunks(resume_id, resume_text)

@app.post("/suggest")
async def suggest_edits(req: AnalyzeReq):
    resume_id = req.resume_id
    jd_text = req.jd_text

    skills = extract_skills(jd_text)
    db = app.state.db
    cur = db.cursor()

    suggestions = []

    for skill in skills:
        vec = embed(skill)

        # retrieve resume chunks related to the skill
        cur.execute(
            """
            SELECT chunk FROM resume_chunks
            WHERE resume_id = %s
            ORDER BY embedding <-> %s::vector
            LIMIT 3
            """,
            (resume_id, vec)
        )
        rows = cur.fetchall()
        context = "\n".join([row[0] for row in rows]) or "(no relevant resume content found)"

        # prompt engineering
        prompt = f"""You are a professional resume coach.

        The candidate's resume contains the following snippets:

        {context}

        The job description requires the skill: {skill}

        Suggest ONE bullet point the candidate could add to better highlight this skill.
        Be honest—only suggest something plausible based on the above content."""

        try:
            suggestion = call_local_llm(prompt)

            suggestions.append({
                "skill": skill,
                "suggestion": suggestion
            })
        except Exception as e:
            suggestions.append({
                "skill": skill,
                "suggestion": f"Error: {str(e)}"
            })
    db.close()
    return {"suggestions": suggestions}

@app.post("/recommend")
def recommend_jobs(req: RecommendRequest):
    skills = extract_skills(req.resume_text)

    with open(JOBS_PATH, "r") as f:
        jobs = json.load(f)

    scored_jobs = []
    for job in jobs:
        score, matched = match_score(skills, job["skills"])
        if score > 0:
            scored_jobs.append({
                "job_id": job["id"],
                "title": job["title"],
                "score": score,
                "matched_skills": matched
            })

    scored_jobs.sort(key=lambda x: x["score"], reverse=True)

    return {
        "skills": skills,
        "recommendations": scored_jobs[:5]
    }