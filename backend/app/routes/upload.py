from fastapi import APIRouter, UploadFile, File
import shutil

router = APIRouter()

@router.post("/")
async def upload_resume(file: UploadFile = File(...)):

    file_location = f"uploads/{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "Resume uploaded successfully",
        "filename": file.filename
    }