from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from core.db import get_db
from middleware.AuthGuard import JWTBearer
from pydantic import BaseModel
from service.PantryService import PantryService
import uuid
from models.Pantry import Pantry, PantryIngredients

router = APIRouter(
    prefix="/pantry",
    tags=["Pantry"],
    dependencies=[Depends(JWTBearer())]
)

class AddIngredientRequest(BaseModel):
    ingredientsid: int
    quantity: int
    
class UpdateIngredientByIngredientIdRequest(BaseModel):
    ingredientsid: int
    quantity: int
    
class DeleteIngredientByIngredientIdRequest(BaseModel):
    ingredientsid: int

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
    userid = int(user["sub"])
    trace_id = str(uuid.uuid4())

    result = await db.execute(
        select(Pantry)
        .options(selectinload(Pantry.pantry_ingredients).selectinload(PantryIngredients.ingredient))
        .where(Pantry.userid == userid)
    )
    pantry = result.scalars().first()
    if not pantry:
        return {
            "trace_id": trace_id,
            "message": "Pantry not found",
            "data": {"ingredients": []}
        }

    ingredients_list = []
    for pi in pantry.pantry_ingredients:
        ingredients_list.append({
            "name": pi.ingredient.name if pi.ingredient else None,
            "quantity": pi.quantity
        })

    return {
        "trace_id": trace_id,
        "message": "success",
        "data": {
            "ingredients": ingredients_list
        }
    }

@router.post("/add-ingredient")
async def add_ingredient(
    payload: AddIngredientRequest,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    user = getattr(request.state, "user", None)
    if not user or "sub" not in user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    userid = int(user["sub"])

    pantries = await PantryService.get_pantry_by_userid(db, userid)
    if not pantries:
        raise HTTPException(status_code=404, detail="Pantry not found")
    pantryid = pantries[0].pantryid

    pantry_ingredient = await PantryService.add_ingredient_to_pantry(
        db, pantryid, payload.ingredientsid, payload.quantity
    )
    if not pantry_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient is not found")

    return {
        "status": "success",
        "message": "Ingredient successfully added.",
        "data": {
            "pantryingredientsid": pantry_ingredient.pantryingredientsid,
            "pantryid": pantry_ingredient.pantryid,
            "ingredientid": pantry_ingredient.ingredientsid,
            "quantity": pantry_ingredient.quantity
        }
    }
    
@router.put("/update-ingredient")
async def update_ingredient_by_ingredientid(
    payload: UpdateIngredientByIngredientIdRequest,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    user = getattr(request.state, "user", None)
    if not user or "sub" not in user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    userid = int(user["sub"])

    pantries = await PantryService.get_pantry_by_userid(db, userid)
    if not pantries:
        raise HTTPException(status_code=404, detail="Pantry not found")
    pantryid = pantries[0].pantryid

    pantry_ingredient = await PantryService.update_pantry_ingredient_by_ingredientid(
        db, pantryid, payload.ingredientsid, payload.quantity
    )
    if not pantry_ingredient:
        raise HTTPException(status_code=404, detail="Pantry ingredient not found")

    return {
        "status": "success",
        "message": "Ingredient successfully updated.",
        "data": {
            "pantryingredientsid": pantry_ingredient.pantryingredientsid,
            "pantryid": pantry_ingredient.pantryid,
            "ingredientid": pantry_ingredient.ingredientsid,
            "quantity": pantry_ingredient.quantity
        }
    }
    
@router.delete("/delete-ingredient")
async def delete_ingredient_by_ingredientid(
    payload: DeleteIngredientByIngredientIdRequest,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    user = getattr(request.state, "user", None)
    if not user or "sub" not in user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    userid = int(user["sub"])

    # Ambil pantry milik user (asumsi satu pantry per user)
    pantries = await PantryService.get_pantry_by_userid(db, userid)
    if not pantries:
        raise HTTPException(status_code=404, detail="Pantry not found")
    pantryid = pantries[0].pantryid

    deleted = await PantryService.delete_pantry_ingredient_by_ingredientid(
        db, pantryid, payload.ingredientsid
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="Pantry ingredient not found")

    return {
        "status": "success",
        "message": "Ingredient successfully deleted.",
        "data": {
            "pantryingredientsid": deleted.pantryingredientsid,
            "pantryid": deleted.pantryid,
            "ingredientid": deleted.ingredientsid,
            "quantity": deleted.quantity
        }
    }