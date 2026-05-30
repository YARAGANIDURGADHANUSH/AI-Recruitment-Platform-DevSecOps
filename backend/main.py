from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

from app.routes import (
    jobs,
    candidates,
    upload,
    ai,
    download,
    insights,
    email,
    auth
)

from database import Base, engine


# ======================================
# CREATE DATABASE TABLES
# ======================================

Base.metadata.create_all(bind=engine)


# ======================================
# FASTAPI APP
# ======================================

app = FastAPI()


# ======================================
# STATIC FILES
# ======================================

# Serve uploaded resumes

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)


# ======================================
# CORS
# ======================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ======================================
# HOME ROUTE
# ======================================

@app.get("/")
def home():

    return {

        "message":
        "AI Recruitment Platform Backend Running"
    }


# ======================================
# JOB ROUTES
# ======================================

app.include_router(

    jobs.router,

    prefix="/jobs",

    tags=["Jobs"]
)


# ======================================
# CANDIDATE ROUTES
# ======================================

app.include_router(

    candidates.router,

    prefix="/candidates",

    tags=["Candidates"]
)


# ======================================
# UPLOAD ROUTES
# ======================================

app.include_router(

    upload.router,

    prefix="/upload",

    tags=["Upload"]
)


# ======================================
# AI RESUME SCORING
# ======================================

app.include_router(

    ai.router,

    prefix="/ai",

    tags=["AI Resume Scoring"]
)


# ======================================
# DOWNLOAD RESUME
# ======================================

app.include_router(

    download.router,

    prefix="/download",

    tags=["Download"]
)


# ======================================
# AI INSIGHTS ROUTES
# ======================================

app.include_router(

    insights.router,

    prefix="/insights",

    tags=["AI Insights"]
)


# ======================================
# EMAIL ROUTES
# ======================================

app.include_router(

    email.router,

    prefix="/email",

    tags=["Email System"]
)


# ======================================
# AUTH ROUTES
# ======================================

app.include_router(

    auth.router,

    prefix="/auth",

    tags=["Authentication"]
)