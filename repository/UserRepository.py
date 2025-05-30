from sqlalchemy.future import select
from models.User import User
from sqlalchemy.ext.asyncio import AsyncSession

class UserRepository:
    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str):
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_user(db: AsyncSession, username: str, email: str, hashed_password: str):
        user = User(username=username, email=email, password=hashed_password)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user