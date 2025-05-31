from sqlalchemy import Column, Integer, String
from models import Base

class DietaryRestriction(Base):
    __tablename__ = "dietaryrestriction"
    dietaryrestrictionid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)