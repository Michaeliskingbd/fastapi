from passlib.context import CryptContext
#Imports a password hashing manager.
#CryptContext lets you define hashing algorithms (e.g., bcrypt) and handles hashing + verification.

from datetime import datetime, timedelta
#datetime.utcnow() → current UTC time
#timedelta(...) → used to add expiration time to tokens
from jose import jwt, JWTError
#from jose import jwt(better than pyjwt)

from src.config import settings
#Loads your environment variables:
#SECRET_KEY
#ALGORITHM
#ACCESS_TOKEN_EXPIRE_MINUTES

##This importations are for HTTP bearer authentication 
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import SessionLocal
from src.auth.models import User
security = HTTPBearer()
#Till this point




pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)
#Configures password hashing.
#schemes=["argon"] → use argon algorithm
#deprecated="auto" → automatically upgrade weaker hashes if needed

async def get_session():
    async with SessionLocal() as session:
        yield session


def hash_password(password: str):
    #def hash_password(password: str) -> str:
    return pwd_context.hash(password)
    #Takes the raw password and returns a secure hash.
    #This is what you store in the database.


def verify_password(plain_password, hashed_password):
    #Compares: plain password (user input) with hashed password (from DB)
    return pwd_context.verify(plain_password, hashed_password)
    #True → password is correct
    #False → invalid password

# JWT creation
def create_access_token(data: dict) -> str:
    #Function to generate a JWT.
    #data = payload (e.g. { "sub": user_id })
    to_encode = data.copy()
    #Makes a copy of the input data.
    #Prevents modifying the original dictionary
    

    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    #Calculates expiration time.
    #Example:
    #now = 10:00
    #expire = 11:00 (if 60 minutes)

    to_encode.update({"exp": expire})
    #Adds "exp" field to payload.
    #"exp" = standard JWT expiration claim.
    #After this time → token becomes invalid.

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    #Creates the JWT string.
    #Uses:
    #payload (to_encode)
    #secret key (for signing)
    #algorithm (e.g. HS256)

    return encoded_jwt
    #Returns the final token (a long encoded string).
    #This is what you send to the client.



    #HTTP Bearer Authentication
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_session)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalid or expired")

    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user



# Refresh_Token
import secrets
import hashlib

REFRESH_TOKEN_BYTES = 64  # 512-bit token


def generate_refresh_token() -> str:
    return secrets.token_urlsafe(REFRESH_TOKEN_BYTES)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


