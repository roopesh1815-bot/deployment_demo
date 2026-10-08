from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    rollno: str
    name: str
    class_name: str
    mobileno: str
    emailid: EmailStr
    password: str


class UserLogin(BaseModel):
    rollno: str
    password: str