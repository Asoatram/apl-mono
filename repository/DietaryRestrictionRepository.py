from models.DietaryRestriction import DietaryRestriction

class DietaryRestrictionRepository:
    @staticmethod
    async def create_dietary_restriction(db, name, description):
        dietary = DietaryRestriction(name=name, description=description)
        db.add(dietary)
        await db.commit()
        await db.refresh(dietary)
        return dietary