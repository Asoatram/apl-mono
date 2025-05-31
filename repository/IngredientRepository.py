from models.Ingredients import Ingredients
from sqlalchemy import select

class IngredientRepository:
    @staticmethod
    async def get_ingredients(db, search=None):
        query = select(Ingredients)
        if search:
            query = query.where(Ingredients.name.op("~*")(search))
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def create_ingredient(db, ingredient_slug):
        # Cek apakah sudah ada
        result = await db.execute(select(Ingredients).where(Ingredients.name == ingredient_slug))
        existing = result.scalar_one_or_none()
        if existing:
            return None  # Sudah ada
        ingredient = Ingredients(name=ingredient_slug)
        db.add(ingredient)
        await db.commit()
        await db.refresh(ingredient)
        return ingredient