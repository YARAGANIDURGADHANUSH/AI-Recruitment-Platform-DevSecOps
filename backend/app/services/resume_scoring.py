from PyPDF2 import PdfReader

required_skills = [
    "Python",
    "Docker",
    "Kubernetes",
    "AWS",
    "CI/CD",
    "FastAPI"
]

def extract_text_from_pdf(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text


def score_resume(resume_text):

    matched_skills = []

    for skill in required_skills:

        if skill.lower() in resume_text.lower():
            matched_skills.append(skill)

    score = int((len(matched_skills) / len(required_skills)) * 100)

    missing_skills = [
        skill for skill in required_skills
        if skill not in matched_skills
    ]

    return {
        "match_score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }