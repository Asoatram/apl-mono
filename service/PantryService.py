import uuid

from repository.PantryRepository import PantryRepository

class PantryService:
    @staticmethod
    async def create_pantry(db, userid):
        return await PantryRepository.create_pantry(db, userid)

    @staticmethod
    async def get_pantry_by_userid(db, userid):
        trace_id = str(uuid.uuid4())
        pantry = await PantryRepository.get_pantry_ingredients_by_userid(db, userid)
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

    @staticmethod
    async def add_ingredient_to_pantry(db, pantryid, ingredientsid, quantity):
        return await PantryRepository.add_ingredient_to_pantry(db, pantryid, ingredientsid, quantity)
    
    @staticmethod
    async def update_pantry_ingredient_by_ingredientid(db, pantryid, ingredientid, quantity):
        return await PantryRepository.update_pantry_ingredient_by_ingredientid(db, pantryid, ingredientid, quantity)
    
    @staticmethod
    async def delete_pantry_ingredient_by_ingredientid(db, pantryid, ingredientid):
        return await PantryRepository.delete_pantry_ingredient_by_ingredientid(db, pantryid, ingredientid)