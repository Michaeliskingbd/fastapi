# schema.py
from pydantic import BaseModel

class AuthCreate(BaseModel):
    email: str
    username: str
    hashed_password: int
    is_verified: bool
    is_active: bool
  