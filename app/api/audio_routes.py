from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.services.audio_service import AudioService


router = APIRouter(
    prefix="/audio",
    tags=["audio"]
)


@router.get("/files")
async def get_audio_files(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> list[dict]:
    files = await AudioService.get_user_files(current_user.id, db)
    return [
        {"filename": file.filename, "path": file.filepath}
        for file in files
    ]


@router.post("/upload")
async def upload_audio_file(
    file: UploadFile = File(...),
    name: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> dict:
    audio = await AudioService.upload_file(
        user_id=current_user.id,
        file=file,
        name=name,
        db=db
    )
    return {
        "id": audio.id,
        "filename": audio.filename,
        "path": audio.filepath
    }
