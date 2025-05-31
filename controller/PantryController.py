from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_db
from middleware.AuthGuard import JWTBearer

from service.PantryService import PantryService

router = APIRouter(
    prefix="/pantry",
    tags=["Pantry"],
    dependencies=[Depends(JWTBearer())]
)

@router.post("")
async def create_pantry(request: Request, db: AsyncSession = Depends(get_db)):
    user = getattr(request.state, "user", None)
    if not user or "sub" not in user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        userid = int(user["sub"])
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user id in token")
    pantry = await PantryService.create_pantry(db, userid)
    return {"message": "Pantry created", "pantryid": pantry.pantryid}

@router.get("")
async def get_pantry(request: Request, db: AsyncSession = Depends(get_db)):
    user = request.state.user if hasattr(request.state, "user") else None
    if not user or "sub" not in user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    userid = user["sub"]
    pantries = await PantryService.get_pantry_by_userid(db, userid)
    return {"pantries": [{"pantryid": p.pantryid, "userid": p.userid} for p in pantries]}