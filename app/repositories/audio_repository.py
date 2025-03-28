from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.audio_file import AudioFile


class AudioRepository:
    @staticmethod
    async def get_by_user_id(user_id: int, db: AsyncSession) -> list[AudioFile]:
        result = await db.execute(select(AudioFile).where(AudioFile.user_id == user_id))

        return result.scalars().all()

    @staticmethod
    async def create_audio_file(
        user_id: int,
        filename: str,
        path: str,
        db: AsyncSession
    ) -> AudioFile:
        audio = AudioFile(
            filename=filename,
            filepath=path,
            user_id=user_id
        )
        db.add(audio)
        await db.commit()
        await db.refresh(audio)
        return audio