from fastapi import APIRouter, UploadFile, File
import shutil

from app.services.resume_scoring import (
    extract_text_from_pdf,
    score_resume
)

router = APIRouter()

@router.post("/score")
async def ai_resume_score(file: UploadFile = File(...)):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume_text = extract_text_from_pdf(file_path)

    result = score_resume(resume_text)

    return result