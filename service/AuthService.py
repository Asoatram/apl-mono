from dotenv import load_dotenv
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from repository.UserRepository import UserRepository
import os
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        print(SECRET_KEY)
        return jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    async def register_user(db, username: str, email: str, password: str):
        existing_user = await UserRepository.get_user_by_username(db, username)
        if existing_user:
            raise ValueError("Username already exists")

        hashed_password = AuthService.hash_password(password)
        return await UserRepository.create_user(db, username, email, hashed_password)


    @staticmethod
    async def authenticate_user(db, username: str, password: str):
        user = await UserRepository.get_user_by_username(db, username)
        if not user or not AuthService.verify_password(password, user.password):
            return None
        return user