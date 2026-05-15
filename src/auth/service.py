from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.security import hash_password
from src.auth.schema import AuthCreate

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src.Student.service import get_user_by_email
from src.auth.security import verify_password, create_access_token

from src.auth.models import RefreshToken
from src.auth.security import generate_refresh_token, hash_token
from src.auth.security import create_access_token

from datetime import datetime, timedelta



async def register_user(db: AsyncSession, payload: AuthCreate):

    # check if email exists
    result = await db.execute(
        select(User).where(User.email == payload.email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # check username
    result = await db.execute(
        select(User).where(User.username == payload.username)
    )
    existing_username = result.scalar_one_or_none()

    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    # create user
    user = User(
        email=payload.email,
        username=payload.username,
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password)
    )

    db.add(user)

    await db.commit()
    await db.refresh(user)

    return user


REFRESH_DAYS = 7

async def login_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})

    # refresh token (opaque)
    raw_refresh = generate_refresh_token()
    token_hash = hash_token(raw_refresh)

    db_token = RefreshToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at = datetime.utcnow() + timedelta(days=REFRESH_DAYS)
    )

    db.add(db_token)
    await db.commit()

    return {
        "access_token": token,
        "refresh_token": raw_refresh
    }



#Logout User
async def logout(db: AsyncSession, refresh_token: str):

    token_hash = hash_token(refresh_token)

    result = await db.execute(
        select(RefreshToken).where(RefreshToken.token_hash == token_hash)
    )
    db_token = result.scalar_one_or_none()

    if not db_token:
        return  # don't leak info

    db_token.is_revoked = True
    await db.commit()

from src.auth.security import (
    hash_token,
    generate_refresh_token
)


async def refresh_access_token(
    db: AsyncSession,
    refresh_token: str
):

    token_hash = hash_token(refresh_token)

    result = await db.execute(
        select(RefreshToken).where(
            RefreshToken.token_hash == token_hash
        )
    )

    db_token = result.scalar_one_or_none()

    if not db_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if db_token.is_revoked:
        raise HTTPException(status_code=401, detail="Refresh token revoked")

    if db_token.expires_at < datetime.now(datetime.timezone.utc):
        raise HTTPException(status_code=401, detail="Refresh token expired")

    # revoke old token (rotation)
    db_token.is_revoked = True

    # create new access token
    access_token = create_access_token({
        "sub": str(db_token.user_id)
    })

    # create new refresh token
    new_refresh = generate_refresh_token()

    new_db_token = RefreshToken(
        user_id=db_token.user_id,
        token_hash=hash_token(new_refresh),
        expires_at = datetime.utcnow() + timedelta(days=REFRESH_DAYS),
        
    )

    db.add(new_db_token)

    await db.commit()

    return {
        "access_token": access_token,
        "refresh_token": new_refresh
    }




