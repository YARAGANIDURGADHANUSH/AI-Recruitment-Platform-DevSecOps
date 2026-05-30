from fastapi import APIRouter

from pydantic import BaseModel

from passlib.context import CryptContext

from jose import jwt

from datetime import datetime, timedelta

from database import SessionLocal

from models import Recruiter


router = APIRouter()


# ======================================
# JWT CONFIG
# ======================================

SECRET_KEY = "SUPER_SECRET_KEY"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


# ======================================
# PASSWORD HASHING
# ======================================

pwd_context = CryptContext(

    schemes=["pbkdf2_sha256"],

    deprecated="auto"
)


# ======================================
# REQUEST MODELS
# ======================================

class RecruiterSignup(BaseModel):

    name: str

    email: str

    password: str


class RecruiterLogin(BaseModel):

    email: str

    password: str


# ======================================
# CREATE JWT TOKEN
# ======================================

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({

        "exp": expire
    })

    encoded_jwt = jwt.encode(

        to_encode,

        SECRET_KEY,

        algorithm=ALGORITHM
    )

    return encoded_jwt


# ======================================
# HOME ROUTE
# ======================================

@router.get("/")
def auth_home():

    return {

        "message":
        "Authentication system working"
    }


# ======================================
# RECRUITER SIGNUP
# ======================================

@router.post("/signup")
def recruiter_signup(data: RecruiterSignup):

    db = SessionLocal()

    existing_user = db.query(Recruiter).filter(

        Recruiter.email == data.email

    ).first()

    if existing_user:

        db.close()

        return {

            "error":
            "Email already registered"
        }

    hashed_password = pwd_context.hash(
        data.password
    )

    recruiter = Recruiter(

        name=data.name,

        email=data.email,

        password=hashed_password
    )

    db.add(recruiter)

    db.commit()

    db.refresh(recruiter)

    db.close()

    return {

        "message":
        "Recruiter account created successfully",

        "recruiter": {

            "id": recruiter.id,

            "name": recruiter.name,

            "email": recruiter.email
        }
    }


# ======================================
# RECRUITER LOGIN
# ======================================

@router.post("/login")
def recruiter_login(data: RecruiterLogin):

    db = SessionLocal()

    recruiter = db.query(Recruiter).filter(

        Recruiter.email == data.email

    ).first()

    if not recruiter:

        db.close()

        return {

            "error":
            "Invalid email or password"
        }

    valid_password = pwd_context.verify(

        data.password,

        recruiter.password
    )

    if not valid_password:

        db.close()

        return {

            "error":
            "Invalid email or password"
        }

    # CREATE JWT TOKEN

    access_token = create_access_token({

        "sub": recruiter.email
    })

    db.close()

    return {

        "message":
        "Login successful",

        "access_token": access_token,

        "token_type": "bearer",

        "recruiter": {

            "id": recruiter.id,

            "name": recruiter.name,

            "email": recruiter.email
        }
    }