from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from parsers import extract_resume_text
from groq_utils import analyze_resume, match_roles
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

with open("job_listings.json") as f:
    JOBS = json.load(f)

@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request, file: UploadFile):
    content = await file.read()
    resume_text = extract_resume_text(content, file.filename)
    resume_info = analyze_resume(resume_text)
    matches = match_roles(resume_info.get("skills", []), JOBS)
    return templates.TemplateResponse("result.html", {
        "request": request,
        "resume": resume_info,
        "matches": matches
    })