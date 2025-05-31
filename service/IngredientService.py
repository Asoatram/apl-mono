from repository.IngredientRepository import IngredientRepository

class IngredientService:
    @staticmethod
    async def get_ingredients(db, search=None):
        return await IngredientRepository.get_ingredients(db, search)