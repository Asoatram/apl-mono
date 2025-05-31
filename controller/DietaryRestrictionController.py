from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_db
from pydantic import BaseModel
from service.DietaryRestrictionService import DietaryRestrictionService
from middleware.AuthGuard import JWTBearer

router = APIRouter(
    prefix="/dietaryrestriction",
    tags=["DietaryRestriction"],
    dependencies=[Depends(JWTBearer())]
)

class DietaryRestrictionRequest(BaseModel):
    name: str
    description: str

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