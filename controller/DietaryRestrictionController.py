from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_db
from pydantic import BaseModel
from service.DietaryRestrictionService import DietaryRestrictionService
from middleware.AuthGuard import JWTBearer
from models.DietaryRestriction import DietaryRestriction, UserDietaryRestriction
from models.User import User
from sqlalchemy import select

router = APIRouter(
    prefix="/dietaryrestriction",
    tags=["DietaryRestriction"],
    dependencies=[Depends(JWTBearer())]
)

class DietaryRestrictionRequest(BaseModel):
    name: str
    description: str

class UserDietaryRestrictionRequest(BaseModel):
    dietaryrestrictionid: int

@router.post("")
async def create_dietary_restriction(
    payload: DietaryRestrictionRequest,
    db: AsyncSession = Depends(get_db)
):
    dietary = await DietaryRestrictionService.create_dietary_restriction(
        db, payload.name, payload.description
    )
    return {
        "status": "success",
        "message": "Dietary restriction successfully added.",
        "data": {
            "dietaryrestrictionid": dietary.dietaryrestrictionid,
            "name": dietary.name,
            "description": dietary.description
        }
    }
    
@router.post("/add-to-user")
async def add_user_dietary_restriction(
    payload: UserDietaryRestrictionRequest,
    db: AsyncSession = Depends(get_db),
    request: Request = None
):
    user = getattr(request.state, "user", None)
    if not user or "sub" not in user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    userid = int(user["sub"])

    # Cek apakah dietaryrestrictionid valid
    result = await db.execute(select(DietaryRestriction).where(DietaryRestriction.dietaryrestrictionid == payload.dietaryrestrictionid))
    dietary = result.scalar_one_or_none()
    if not dietary:
        raise HTTPException(status_code=404, detail="Dietary restriction not found")

    # Cek apakah sudah ada
    result = await db.execute(
        select(UserDietaryRestriction).where(
            UserDietaryRestriction.userid == userid,
            UserDietaryRestriction.dietaryrestrictionid == payload.dietaryrestrictionid
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="User already has this dietary restriction")

    user_dietary = UserDietaryRestriction(
        userid=userid,
        dietaryrestrictionid=payload.dietaryrestrictionid
    )
    db.add(user_dietary)
    await db.commit()
    await db.refresh(user_dietary)
    return {
        "status": "success",
        "message": "Dietary restriction added to user.",
        "data": {
            "userdietaryrestrictionid": user_dietary.userdietaryrestrictionid,
            "userid": user_dietary.userid,
            "dietaryrestrictionid": user_dietary.dietaryrestrictionid
        }
    }
    
@router.delete("/remove-from-user")
async def remove_user_dietary_restriction(
    payload: UserDietaryRestrictionRequest,
    db: AsyncSession = Depends(get_db),
    request: Request = None
):
    user = getattr(request.state, "user", None)
    if not user or "sub" not in user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    userid = int(user["sub"])

    # Cari relasi user-dietaryrestriction
    result = await db.execute(
        select(UserDietaryRestriction).where(
            UserDietaryRestriction.userid == userid,
            UserDietaryRestriction.dietaryrestrictionid == payload.dietaryrestrictionid
        )
    )
    user_dietary = result.scalar_one_or_none()
    if not user_dietary:
        raise HTTPException(status_code=404, detail="User dietary restriction not found")

    await db.delete(user_dietary)
    await db.commit()
    return {
        "status": "success",
        "message": "Dietary restriction removed from user.",
        "data": {
            "userdietaryrestrictionid": user_dietary.userdietaryrestrictionid,
            "userid": user_dietary.userid,
            "dietaryrestrictionid": user_dietary.dietaryrestrictionid
        }
    }