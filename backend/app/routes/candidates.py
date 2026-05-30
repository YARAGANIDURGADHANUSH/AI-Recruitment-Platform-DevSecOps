from fastapi import APIRouter, Query

from database import SessionLocal
from models import Candidate

router = APIRouter()


# ======================================
# GET ALL CANDIDATES
# ======================================

@router.get("/")
def get_candidates(

    search: str = Query(default=""),

    min_score: int = Query(default=0)

):

    db = SessionLocal()

    candidates = db.query(Candidate).all()

    result = []

    for candidate in candidates:

        # SEARCH FILTER
        matches_search = (

            search.lower() in candidate.name.lower()

            or

            search.lower() in candidate.skills.lower()

        )

        # SCORE FILTER
        matches_score = candidate.score >= int(min_score)

        if matches_search and matches_score:

            result.append({

                "id": candidate.id,

                "filename": candidate.filename,

                "name": candidate.name,

                "email": candidate.email,

                "phone": candidate.phone,

                "skills": candidate.skills,

                "score": candidate.score,

                "status": candidate.status

            })

    # SORT BY HIGHEST SCORE
    result = sorted(

        result,

        key=lambda x: x["score"],

        reverse=True

    )

    db.close()

    return result


# ======================================
# ANALYTICS DASHBOARD
# ======================================

@router.get("/analytics")
def candidate_analytics():

    db = SessionLocal()

    candidates = db.query(Candidate).all()

    total_candidates = len(candidates)

    shortlisted = len([
        c for c in candidates
        if c.status == "Shortlisted"
    ])

    rejected = len([
        c for c in candidates
        if c.status == "Rejected"
    ])

    pending = len([
        c for c in candidates
        if c.status == "Pending"
    ])

    # AVERAGE SCORE
    if total_candidates > 0:

        average_score = int(

            sum(c.score for c in candidates)

            /

            total_candidates
        )

    else:

        average_score = 0

    # TOP CANDIDATE
    top_candidate = None

    if total_candidates > 0:

        best = max(
            candidates,
            key=lambda c: c.score
        )

        top_candidate = {

            "name": best.name,

            "score": best.score
        }

    db.close()

    return {

        "total_candidates": total_candidates,

        "shortlisted": shortlisted,

        "rejected": rejected,

        "pending": pending,

        "average_score": average_score,

        "top_candidate": top_candidate
    }


# ======================================
# AI CANDIDATE INSIGHTS
# ======================================

@router.get("/insights/{candidate_id}")
def candidate_insights(candidate_id: int):

    db = SessionLocal()

    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id
    ).first()

    if not candidate:

        db.close()

        return {
            "message": "Candidate not found"
        }

    # MATCHED SKILLS
    matched = []

    if candidate.matched_skills:

        matched = candidate.matched_skills.split(",")

    # MISSING SKILLS
    missing = []

    if candidate.missing_skills:

        missing = candidate.missing_skills.split(",")

    # STRENGTHS
    strengths = []

    for skill in matched:

        strengths.append(
            f"Strong knowledge of {skill.strip()}"
        )

    # WEAKNESSES
    weaknesses = []

    for skill in missing:

        weaknesses.append(
            f"Missing {skill.strip()}"
        )

    # HIRING CONFIDENCE
    confidence = candidate.score

    # RECOMMENDATION
    if candidate.score >= 80:

        recommendation = (
            "Highly recommended for interview"
        )

        readiness = "Excellent"

    elif candidate.score >= 60:

        recommendation = (
            "Good candidate for interview"
        )

        readiness = "Good"

    elif candidate.score >= 40:

        recommendation = (
            "Consider after skill improvement"
        )

        readiness = "Moderate"

    else:

        recommendation = (
            "Not recommended currently"
        )

        readiness = "Low"

    db.close()

    return {

        "candidate_name": candidate.name,

        "score": candidate.score,

        "strengths": strengths,

        "weaknesses": weaknesses,

        "recommendation": recommendation,

        "hiring_confidence": confidence,

        "interview_readiness": readiness
    }


# ======================================
# SHORTLIST CANDIDATE
# ======================================

@router.put("/shortlist/{candidate_id}")
def shortlist_candidate(candidate_id: int):

    db = SessionLocal()

    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id
    ).first()

    if candidate:

        candidate.status = "Shortlisted"

        db.commit()

    db.close()

    return {
        "message": "Candidate shortlisted"
    }


# ======================================
# REJECT CANDIDATE
# ======================================

@router.put("/reject/{candidate_id}")
def reject_candidate(candidate_id: int):

    db = SessionLocal()

    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id
    ).first()

    if candidate:

        candidate.status = "Rejected"

        db.commit()

    db.close()

    return {
        "message": "Candidate rejected"
    }


# ======================================
# RESET STATUS
# ======================================

@router.put("/reset/{candidate_id}")
def reset_candidate(candidate_id: int):

    db = SessionLocal()

    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id
    ).first()

    if candidate:

        candidate.status = "Pending"

        db.commit()

    db.close()

    return {
        "message": "Candidate reset"
    }