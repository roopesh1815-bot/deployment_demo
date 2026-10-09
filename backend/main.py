```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import User
from schemas import UserRegister, UserLogin


app = FastAPI(
    title="Student Registration API",
    description="API for student registration and login",
    version="1.0.0"
)


# Create database tables if they do not exist.
Base.metadata.create_all(bind=engine)


# Allow requests from the deployed Vercel frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://my-project-6yo0srnjr-roopz.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database session dependency.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Backend health check.
@app.get("/")
def home():
    return {"message": "Backend is running"}


# Register a new student.
@app.post("/register")
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):
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


# Log in an existing student.
@app.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.rollno == user.rollno
    ).first()

    if (
        not existing_user
        or existing_user.password != user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid roll number or password"
        )

    return {
        "message": "Login successful",
        "rollno": existing_user.rollno,
        "name": existing_user.name
    }
```
