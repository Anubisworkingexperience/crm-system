from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.db import get_session
from app.auth.repository import UserRepo
from app.auth.jwt_utils import create_access_token

router = APIRouter(prefix="", tags=["auth"])

class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

class AuthOut(BaseModel):
    access_token: str
    token_type: str = "Bearer"

@router.post("/register", response_model=AuthOut, status_code=201)
async def register(data: RegisterIn, session: AsyncSession = Depends(get_session)):
    repo = UserRepo(session)
    try:
        user = await repo.create_user(data.email, data.password)
    except ValueError:
        raise HTTPException(status_code=409, detail="Email already registered")
    token = create_access_token(sub=str(user.id), extra={"email": user.email})
    return AuthOut(access_token=token)

class LoginIn(BaseModel):
    email: EmailStr
    password: str

@router.post("/login", response_model=AuthOut)
async def login(data: LoginIn, session: AsyncSession = Depends(get_session)):
    repo = UserRepo(session)
    user = await repo.verify_credentials(data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(sub=str(user.id), extra={"email": user.email})
    return AuthOut(access_token=token)
