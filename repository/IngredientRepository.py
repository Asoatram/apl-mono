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