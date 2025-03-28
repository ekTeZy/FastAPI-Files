from fastapi import APIRouter
from app.api.auth_routes import router as core_router

router = APIRouter()
router.include_router(core_router)