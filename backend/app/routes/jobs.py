from fastapi import APIRouter

router = APIRouter()

jobs = [
    {
        "id": 1,
        "title": "DevOps Engineer Intern",
        "company": "LVC Solutions"
    },
    {
        "id": 2,
        "title": "Cloud Engineer Intern",
        "company": "AI Tech"
    }
]

@router.get("/")
def get_jobs():
    return jobs