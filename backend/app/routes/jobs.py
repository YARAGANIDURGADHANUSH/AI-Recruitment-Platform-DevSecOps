from fastapi import APIRouter

from database import SessionLocal

from models import Job

from app.services.job_parser import (
    extract_skills_from_jd
)

router = APIRouter()


# ======================================
# CREATE JOB DESCRIPTION
# ======================================

@router.post("/create")
def create_job(job: dict):

    db = SessionLocal()

    # Extract skills from JD
    extracted_skills = extract_skills_from_jd(
        job["description"]
    )

    # Create new job
    new_job = Job(

        title=job["title"],

        description=job["description"],

        required_skills=", ".join(
            extracted_skills
        )
    )

    # Save to PostgreSQL
    db.add(new_job)

    db.commit()

    db.refresh(new_job)

    db.close()

    return {

        "message": "Job created successfully",

        "job_id": new_job.id,

        "required_skills": extracted_skills
    }


# ======================================
# GET ALL JOBS
# ======================================

@router.get("/")
def get_jobs():

    db = SessionLocal()

    jobs = db.query(Job).all()

    result = []

    for job in jobs:

        result.append({

            "id": job.id,

            "title": job.title,

            "description": job.description,

            "required_skills": job.required_skills
        })

    db.close()

    return result