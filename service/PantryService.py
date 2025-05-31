from repository.PantryRepository import PantryRepository

class PantryService:
    @staticmethod
    async def create_pantry(db, userid):
        return await PantryRepository.create_pantry(db, userid)

    @staticmethod
    async def get_pantry_by_userid(db, userid):
        return await PantryRepository.get_pantry_by_userid(db, userid)
    
    @staticmethod
    async def add_ingredient_to_pantry(db, pantryid, ingredientsid, quantity):
        return await PantryRepository.add_ingredient_to_pantry(db, pantryid, ingredientsid, quantity)
    
    @staticmethod
    async def update_pantry_ingredient_by_ingredientid(db, pantryid, ingredientid, quantity):
        return await PantryRepository.update_pantry_ingredient_by_ingredientid(db, pantryid, ingredientid, quantity)
    
    @staticmethod
    async def delete_pantry_ingredient_by_ingredientid(db, pantryid, ingredientid):
        return await PantryRepository.delete_pantry_ingredient_by_ingredientid(db, pantryid, ingredientid)