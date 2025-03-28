from fastapi import APIRouter, Depends, Request, HTTPException, Header
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import jwt

from app.auth import yandex
from app.auth.token import create_access_token
from app.core.config import settings
from app.database import get_db
from app.models.user import User
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.get("/yandex")
async def auth_yandex() -> RedirectResponse:
    redirect_url: str = yandex.get_yandex_oauth_url()
    return RedirectResponse(url=redirect_url)


@router.get("/yandex/callback")
async def yandex_callback(request: Request, db: AsyncSession = Depends(get_db)) -> JSONResponse:
    code: str | None = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Code not provided")

    token_data: dict = await yandex.exchange_code_for_token(code)
    access_token: str | None = token_data.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=400, detail="Access token not received")

    user_info: dict = await yandex.get_yandex_user_info(access_token)
    yandex_id: str = user_info.get("id")
    username: str = user_info.get("login")
    email: str = user_info.get("default_email")

    result = await db.execute(select(User).where(User.yandex_id == yandex_id))
    user: User | None = result.scalar_one_or_none()

    if user is None:
        user = User(
            yandex_id=yandex_id,
            username=username,
            email=email,
            access_token=access_token,
        )
        db.add(user)
    else:
        user.access_token = access_token

    await db.commit()
    internal_token: str = create_access_token({"sub": str(user.id)})
    return JSONResponse(content={"access_token": internal_token})


@router.post("/refresh-token")
async def refresh_token(authorization: str = Header(...)) -> JSONResponse:
    try:
        token: str = authorization.replace("Bearer ", "")
        payload: dict = jwt.decode(
            token, settings.API_SECRET_KEY, algorithms=["HS256"])
        user_id: str | None = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    new_token: str = create_access_token({"sub": user_id})
    return JSONResponse(content={"access_token": new_token})


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)) -> dict:
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "yandex_id": current_user.yandex_id,
    }
