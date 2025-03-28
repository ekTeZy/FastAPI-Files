from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    @staticmethod
    async def get_user_by_id(user_id: int, db: AsyncSession) -> User:
        user = await UserRepository.get_by_id(user_id, db)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
