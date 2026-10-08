from sqlalchemy import Column, String

from database import Base


class User(Base):
    __tablename__ = "users"

    rollno = Column(String(20), primary_key=True)
    name = Column(String(100), nullable=False)
    class_name = Column("class", String(50), nullable=False)
    mobileno = Column(String(15), nullable=False)
    emailid = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)