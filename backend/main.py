from fastapi import FastAPI
from fastapi import UploadFile, File
from backend.parsers.pdf_parser import parse_pdf

app = FastAPI()

@app.get("/healthz")

def health():
    return {"status": "ok"}

@app.post("/parse-resume")
async def parse_resume(file: UploadFile = File(...)):
    content = await file.read()
    return parse_pdf(content)
