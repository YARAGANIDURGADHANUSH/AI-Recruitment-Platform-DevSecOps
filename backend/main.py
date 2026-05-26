from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import jobs, candidates, upload, ai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AI Recruitment Platform Backend Running"}

app.include_router(
    jobs.router,
    prefix="/jobs",
    tags=["Jobs"]
)

app.include_router(
    candidates.router,
    prefix="/candidates",
    tags=["Candidates"]
)

app.include_router(
    upload.router,
    prefix="/upload",
    tags=["Upload"]
)

app.include_router(
    ai.router,
    prefix="/ai",
    tags=["AI Resume Scoring"]
)