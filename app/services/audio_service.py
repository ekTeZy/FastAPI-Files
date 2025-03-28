from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.audio_repository import AudioRepository
from app.models.audio_file import AudioFile

class AudioService:
    @staticmethod
    async def get_user_files(user_id: int, db: AsyncSession) -> list[AudioFile]:
        return await AudioRepository.get_by_user_id(user_id, db)