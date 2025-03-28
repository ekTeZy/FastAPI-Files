from datetime import datetime, timedelta
import jwt
from app.core.config import settings


def create_access_token(data: dict) -> str:
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    payload.update({"exp": expire})
    return jwt.encode(payload, settings.API_SECRET_KEY, algorithm="HS256")
