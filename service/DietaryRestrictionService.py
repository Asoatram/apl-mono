from repository.DietaryRestrictionRepository import DietaryRestrictionRepository

class DietaryRestrictionService:
    @staticmethod
    async def create_dietary_restriction(db, name, description):
        return await DietaryRestrictionRepository.create_dietary_restriction(db, name, description)