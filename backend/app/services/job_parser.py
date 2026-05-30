import re


SKILLS_DATABASE = [

    "Python",
    "AWS",
    "Docker",
    "Kubernetes",
    "FastAPI",
    "React",
    "JavaScript",
    "SQL",
    "CI/CD",
    "Linux",
    "Git",
    "NLP",
    "Machine Learning",
    "AI",
    "DevOps"
]


def extract_skills_from_jd(job_text):

    found_skills = []

    for skill in SKILLS_DATABASE:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(
            pattern,
            job_text,
            re.IGNORECASE
        ):

            found_skills.append(skill)

    return found_skills