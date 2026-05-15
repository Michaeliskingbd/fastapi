from fastapi import APIRouter, Depends
from src.db.session import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.schema import AuthCreate, AuthResponse,loginCreate
from src.auth.service import register_user,login_user
from src.auth.security import get_current_user
from src.auth.service import refresh_access_token, logout

router = APIRouter()


async def get_session():
    async with SessionLocal() as session:
        yield session
   

@router.post("/register", response_model=AuthResponse)
async def register(payload: AuthCreate, db: AsyncSession =  Depends(get_session)):

    user = await register_user(db, payload)
    return user


@router.post("/login")
async def login(
    data: loginCreate,
    session: AsyncSession = Depends(get_session)
):
    token = await login_user(session, data.email, data.password)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/refresh")
async def refresh(refresh_token: str, db: AsyncSession = Depends(get_session)):
    return await refresh_access_token(db, refresh_token)


@router.post("/logout")
async def logout_user(refresh_token: str, db: AsyncSession = Depends(get_session)):
    await logout(db, refresh_token)
    return {"message": "Logged out"}

@router.get("/me")
async def me(current_user=Depends(get_current_user)):
    return current_user