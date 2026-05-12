# schema.py
from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    course: str
    age: int
    gender: str
    location: str
    phone: str