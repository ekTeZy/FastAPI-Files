from typing import Optional
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

    @staticmethod
    async def update_user(
        user_id: int, db: AsyncSession, username: Optional[str] = None, email: Optional[str] = None
    ) -> User:
        user = await UserRepository.update_user_data(user_id, db, username, email)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return user
    
    @staticmethod
    async def delete_user(user_id: int, db: AsyncSession) -> None:
        success = await UserRepository.delete_by_id(user_id, db)
        
        if not success:
            raise HTTPException(status_code=404, detail="User not found")

        return success