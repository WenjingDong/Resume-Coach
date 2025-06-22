from fastapi import FastAPI
from fastapi import HTTPException, status, UploadFile, File
from backend.parsers.pdf_parser import parse_pdf

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
