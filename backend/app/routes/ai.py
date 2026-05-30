from fastapi import APIRouter, UploadFile, File
import shutil

from app.services.resume_scoring import (
    extract_text_from_pdf,
    score_resume
)

from app.services.resume_parser import (
    extract_email,
    extract_phone,
    extract_name,
    extract_skills
)

from database import SessionLocal
from models import Candidate

router = APIRouter()


@router.post("/score")
async def ai_resume_score(
    file: UploadFile = File(...)
):

    # SAVE FILE
    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    # EXTRACT TEXT
    resume_text = extract_text_from_pdf(
        file_path
    )

    # AI SCORE
    result = score_resume(
        resume_text
    )

    # EXTRACT DETAILS
    candidate_name = extract_name(
        resume_text
    )

    candidate_email = extract_email(
        resume_text
    )

    candidate_phone = extract_phone(
        resume_text
    )

    candidate_skills = extract_skills(
        resume_text
    )

    # DATABASE
    db = SessionLocal()

    # CREATE CANDIDATE
    candidate = Candidate(

        filename=file.filename,

        name=candidate_name,

        email=candidate_email,

        phone=candidate_phone,

        skills=", ".join(candidate_skills),

        matched_skills=", ".join(
            result["matched_skills"]
        ),

        missing_skills=", ".join(
            result["missing_skills"]
        ),

        score=result["match_score"],

        status="Pending"

    )

    # SAVE
    db.add(candidate)

    db.commit()

    db.refresh(candidate)

    db.close()

    # RETURN RESPONSE
    return {

        "id": candidate.id,

        "match_score": result["match_score"],

        "matched_skills": result["matched_skills"],

        "missing_skills": result["missing_skills"],

        "name": candidate_name,

        "email": candidate_email,

        "phone": candidate_phone,

        "skills": candidate_skills,

        "status": "Pending"

    }