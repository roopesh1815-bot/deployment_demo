from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import User
from schemas import UserRegister
from schemas import UserRegister, UserLogin

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Backend is running"}


@app.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        (User.rollno == user.rollno) |
        (User.emailid == user.emailid)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Roll number or email already registered"
        )

    new_user = User(
        rollno=user.rollno,
        name=user.name,
        class_name=user.class_name,
        mobileno=user.mobileno,
        emailid=user.emailid,
        password=user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Registration successful",
        "rollno": new_user.rollno
    }
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.rollno == user.rollno
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid roll number or password"
        )

    if existing_user.password != user.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid roll number or password"
        )

    return {
        "message": "Login successful",
        "rollno": existing_user.rollno,
        "name": existing_user.name
    }
