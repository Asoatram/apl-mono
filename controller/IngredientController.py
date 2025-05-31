from fastapi import APIRouter, Depends, Query, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from service.IngredientService import IngredientService
from core.db import get_db
from middleware.AuthGuard import JWTBearer
from pydantic import BaseModel
import uuid

router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredients"],
    dependencies=[Depends(JWTBearer())]
)

class IngredientCreateRequest(BaseModel):
    ingredient_slug: str

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
        
@router.post("")
async def create_ingredient(
    payload: IngredientCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    ingredient = await IngredientService.create_ingredient(db, payload.ingredient_slug)
    if ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient is not found or already exists")
    return {"message": "Successfully added new ingredients"}