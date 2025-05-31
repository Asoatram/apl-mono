from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from repository.RecipeRepository import RecipeRepository
from service.AuthService import AuthService
from core.db import get_db

router = APIRouter()

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/register")
async def register_user(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    try:
        user = await AuthService.register_user(db, payload.username, payload.email, payload.password)
        token = AuthService.create_access_token(data={
            "sub": str(user.userid),
            "username": user.username
        })
        return {"message": f"User {user.username} registered successfully", "access_token": token}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenResponse)
async def login_user(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await AuthService.authenticate_user(db, payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = AuthService.create_access_token(data={
        "sub": str(user.userid),
        "username": user.username
    })
    return TokenResponse(access_token=token)