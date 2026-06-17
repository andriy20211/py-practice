from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from utils.security import get_password_hash

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def create_user(self, email: str, password: str, role: str = "user") -> User:
        hashed_password = get_password_hash(password)
        new_user = User(email=email, hashed_password=hashed_password, role=role)
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user