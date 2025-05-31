from repository.IngredientRepository import IngredientRepository

class IngredientService:
    @staticmethod
    async def get_ingredients(db, search=None):
        return await IngredientRepository.get_ingredients(db, search)
    
    @staticmethod
    async def create_ingredient(db, ingredient_slug):
        return await IngredientRepository.create_ingredient(db, ingredient_slug)