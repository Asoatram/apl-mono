from fastapi import APIRouter, Depends, Query, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from service.IngredientService import IngredientService
from core.db import get_db
from middleware.AuthGuard import JWTBearer
import uuid

router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredients"],
    dependencies=[Depends(JWTBearer())]
)

@router.get("")
async def get_ingredients(
    request: Request,
    search: str = Query(None, description="Regex search for ingredient name"),
    db: AsyncSession = Depends(get_db)
):
    trace_id = request.headers.get("X-Trace-Id") or str(uuid.uuid4())
    try:
        ingredients = await IngredientService.get_ingredients(db, search)
        return {
            "trace_id": trace_id,
            "message": "success",
            "data": {
                "ingredients": [{"name": ing.name} for ing in ingredients]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "trace_id": trace_id,
            "message": f"error: {str(e)}",
            "data": {"ingredients": []}
        })