from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models import Base

class Pantry(Base):
    __tablename__ = "pantry"
    pantryid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    userid = Column(Integer, ForeignKey("users.userid"), nullable=False)

    user = relationship("User", back_populates="pantries")