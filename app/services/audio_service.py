from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.audio_repository import AudioRepository
from app.repositories.audio_repository import AudioRepository
from app.models.audio_file import AudioFile
from fastapi import UploadFile
import os

AUDIO_DIR = "static/audio"

class AudioService:
    @staticmethod
    async def get_user_files(user_id: int, db: AsyncSession) -> list[AudioFile]:
        return await AudioRepository.get_by_user_id(user_id, db)

    @staticmethod
    async def upload_file(
        user_id: int,
        file: UploadFile,
        name: str,
        db: AsyncSession
    ) -> AudioFile:
        os.makedirs(AUDIO_DIR, exist_ok=True)

        filename = f"{user_id}_{file.filename}"  # чтобы избежать конфликтов
        path = os.path.join(AUDIO_DIR, filename)

        with open(path, "wb") as f:
            content = await file.read()
            f.write(content)

        return await AudioRepository.create_audio_file(
            user_id=user_id,
            filename=name,
            path=path,
            db=db
        )
