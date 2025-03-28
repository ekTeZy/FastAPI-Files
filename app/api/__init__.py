from fastapi import APIRouter
from app.api.auth_routes import router as core_router
from app.api.audio_routes import router as audio_router

router = APIRouter()

router.include_router(audio_router)
router.include_router(core_router)
