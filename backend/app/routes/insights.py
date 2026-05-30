from fastapi import APIRouter

from database import SessionLocal
from models import Candidate

router = APIRouter()


@router.get("/{candidate_id}")
def get_candidate_insights(candidate_id: int):

    db = SessionLocal()

    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id
    ).first()

    if not candidate:

        return {
            "error": "Candidate not found"
        }

    matched_skills = []

    missing_skills = []

    if candidate.matched_skills:

        matched_skills = candidate.matched_skills.split(",")

    if candidate.missing_skills:

        missing_skills = candidate.missing_skills.split(",")

    # ======================================
    # HIRING CONFIDENCE
    # ======================================

    if candidate.score >= 80:

        hiring_confidence = 95

        recommendation = (
            "Strong candidate. Recommended for immediate interview."
        )

        interview_readiness = "High"

    elif candidate.score >= 60:

        hiring_confidence = 75

        recommendation = (
            "Good candidate with moderate skill alignment."
        )

        interview_readiness = "Medium"

    else:

        hiring_confidence = 45

        recommendation = (
            "Candidate requires additional training."
        )

        interview_readiness = "Low"

    # ======================================
    # TRAINING RECOMMENDATIONS
    # ======================================

    training_recommendations = []

    for skill in missing_skills:

        training_recommendations.append(
            f"Improve knowledge in {skill.strip()}"
        )

    db.close()

    return {

        "candidate_name": candidate.name,

        "score": candidate.score,

        "status": candidate.status,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "hiring_confidence": hiring_confidence,

        "interview_readiness": interview_readiness,

        "recommendation": recommendation,

        "strengths": matched_skills,

        "weaknesses": missing_skills,

        "training_recommendations":
            training_recommendations
    }