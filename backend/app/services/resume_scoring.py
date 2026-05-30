from PyPDF2 import PdfReader

from database import SessionLocal

from models import Job


# ======================================
# EXTRACT TEXT FROM PDF
# ======================================

def extract_text_from_pdf(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        text += page.extract_text()

    return text


# ======================================
# GET LATEST JOB SKILLS
# ======================================

def get_latest_job_skills():

    db = SessionLocal()

    latest_job = db.query(Job).order_by(
        Job.id.desc()
    ).first()

    db.close()

    # If no job uploaded yet
    if not latest_job:

        return [

            "Python",
            "Docker",
            "Kubernetes",
            "AWS",
            "CI/CD",
            "FastAPI"

        ]

    return latest_job.required_skills.split(",")


# ======================================
# AI RESUME SCORING
# ======================================

def score_resume(resume_text):

    required_skills = get_latest_job_skills()

    matched_skills = []

    for skill in required_skills:

        if skill.strip().lower() in resume_text.lower():

            matched_skills.append(
                skill.strip()
            )

    # SCORE %
    score = int(

        (
            len(matched_skills)

            /

            len(required_skills)
        ) * 100

    )

    # MISSING SKILLS
    missing_skills = [

        skill.strip()

        for skill in required_skills

        if skill.strip() not in matched_skills

    ]

    # MATCH LABEL
    if score >= 80:

        match_label = "Excellent Match"

    elif score >= 60:

        match_label = "Strong Match"

    elif score >= 40:

        match_label = "Moderate Match"

    else:

        match_label = "Weak Match"

    return {

        "match_score": score,

        "match_label": match_label,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills
    }