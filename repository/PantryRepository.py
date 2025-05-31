from models.Pantry import Pantry
from sqlalchemy import select

class PantryRepository:
    @staticmethod
    async def create_pantry(db, userid):
        pantry = Pantry(userid=userid)
        db.add(pantry)
        await db.commit()
        await db.refresh(pantry)
        return pantry

    @staticmethod
    async def get_pantry_by_userid(db, userid):
        result = await db.execute(select(Pantry).where(Pantry.userid == userid))
        return result.scalars().all()