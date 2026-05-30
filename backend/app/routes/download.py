from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/{filename}")
def download_resume(filename: str):

    file_path = f"uploads/{filename}"

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )