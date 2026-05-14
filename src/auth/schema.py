from pydantic import BaseModel, EmailStr

class AuthCreate(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    password: str

class AuthResponse(BaseModel):
    #id: str
    email: EmailStr
    username: str
    full_name: str
    #is_verified: bool
    is_active: bool


class loginCreate(BaseModel):
    email: EmailStr
    password: str

class loginResponse(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    is_active: bool

class Config:
    from_attributes = True