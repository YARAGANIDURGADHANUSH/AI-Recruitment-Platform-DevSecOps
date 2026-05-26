from fastapi import APIRouter

router = APIRouter()

candidates = [
    {
        "id": 1,
        "name": "John Doe",
        "skill": "DevOps"
    }
]

@router.get("/")
def get_candidates():
    return candidates