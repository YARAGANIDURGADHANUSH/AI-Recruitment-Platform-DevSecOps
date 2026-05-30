from sqlalchemy import Column, Integer, String

from database import Base


# ======================================
# CANDIDATE TABLE
# ======================================

class Candidate(Base):

    __tablename__ = "candidates"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Resume File
    filename = Column(String)

    # Candidate Details
    name = Column(String)

    email = Column(String)

    phone = Column(String)

    # Skills
    skills = Column(String)

    matched_skills = Column(String)

    missing_skills = Column(String)

    # AI Match Score
    score = Column(Integer)

    # Recruiter Status
    status = Column(
        String,
        default="Pending"
    )


# ======================================
# JOB TABLE
# ======================================

class Job(Base):

    __tablename__ = "jobs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Example:
    # DevOps Engineer
    # AI Engineer

    title = Column(String)

    # Full Job Description

    description = Column(String)

    # AI Extracted Skills

    required_skills = Column(String)


# ======================================
# RECRUITER TABLE
# ======================================

class Recruiter(Base):

    __tablename__ = "recruiters"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Recruiter Name

    name = Column(String)

    # Login Email

    email = Column(
        String,
        unique=True,
        index=True
    )

    # Hashed Password

    password = Column(String)

    # Role

    role = Column(
        String,
        default="Recruiter"
    )