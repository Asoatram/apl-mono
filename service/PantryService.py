from repository.PantryRepository import PantryRepository

class PantryService:
    @staticmethod
    async def create_pantry(db, userid):
        return await PantryRepository.create_pantry(db, userid)

    @staticmethod
    async def get_pantry_by_userid(db, userid):
        return await PantryRepository.get_pantry_by_userid(db, userid)