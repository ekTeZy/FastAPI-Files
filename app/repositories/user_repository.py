from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User


class UserRepository:
    @staticmethod
    async def get_by_id(user_id: int, db: AsyncSession) -> User | None:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def update_user_data(
        user_id: int, db: AsyncSession, username: str | None = None, email: str | None = None
    ) -> User:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            return None

        if username is not None:
            user.username = username
        if email is not None:
            user.email = email

        await db.commit()
        await db.refresh(user)
        return user
