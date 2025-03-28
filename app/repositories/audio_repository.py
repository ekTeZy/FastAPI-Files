from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.audio_file import AudioFile


class AudioRepository:
    @staticmethod
    async def get_by_user_id(user_id: int, db: AsyncSession) -> list[AudioFile]:
        result = await db.execute(select(AudioFile).where(AudioFile.user_id == user_id))

        return result.scalars().all()
