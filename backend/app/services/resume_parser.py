import re

def extract_email(text):

    match = re.search(r'[\w\.-]+@[\w\.-]+', text)

    return match.group(0) if match else "Not Found"


def extract_phone(text):

    match = re.search(r'\+?\d[\d\s\-]{8,15}', text)

    return match.group(0) if match else "Not Found"


def extract_name(text):

    lines = text.split('\n')

    for line in lines:

        line = line.strip()

        if len(line.split()) >= 2 and len(line) < 40:
            return line

    return "Unknown"


def extract_skills(text):

    skills_db = [
        "Python",
        "Docker",
        "Kubernetes",
        "AWS",
        "FastAPI",
        "React",
        "SQL",
        "CI/CD",
        "JavaScript"
    ]

    found_skills = []

    for skill in skills_db:

        if skill.lower() in text.lower():
            found_skills.append(skill)

    return found_skills