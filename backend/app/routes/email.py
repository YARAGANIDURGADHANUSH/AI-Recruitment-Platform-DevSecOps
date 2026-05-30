from fastapi import APIRouter

import smtplib

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart

from database import SessionLocal

from models import Candidate


router = APIRouter()


# ======================================
# TEST ROUTE
# ======================================

@router.get("/")
def email_home():

    return {

        "message":
        "Email system working"
    }


# ======================================
# SEND INTERVIEW INVITE
# ======================================

@router.post("/interview/{candidate_id}")
def send_interview_email(candidate_id: int):

    db = SessionLocal()

    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id
    ).first()

    if not candidate:

        db.close()

        return {

            "error":
            "Candidate not found"
        }

    # ======================================
    # EMAIL CONFIG
    # ======================================

    sender_email = "dy402004@gmail.com"

    sender_password = "bjgn zvfa wlqd vkxg"

    receiver_email = candidate.email

    # ======================================
    # EMAIL CONTENT
    # ======================================

    subject = "Interview Invitation - AI Recruitment Platform"

    body = f"""
Dear {candidate.name},

Congratulations!

You have been shortlisted for the next round.

Interview Details:

Role:
AI Engineer

Date:
Monday

Time:
10:00 AM

Meeting Link:
https://meet.google.com/

Regards,
Recruitment Team
"""

    # ======================================
    # CREATE EMAIL
    # ======================================

    message = MIMEMultipart()

    message["From"] = sender_email

    message["To"] = receiver_email

    message["Subject"] = subject

    message.attach(
        MIMEText(body, "plain")
    )

    # ======================================
    # SEND EMAIL
    # ======================================

    try:

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            sender_email,
            sender_password
        )

        server.sendmail(

            sender_email,

            receiver_email,

            message.as_string()
        )

        server.quit()

        db.close()

        return {

            "message":
            f"Interview invite sent to {candidate.email}"
        }

    except Exception as e:

        db.close()

        return {

            "error":
            str(e)
        }