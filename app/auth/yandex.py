import httpx
from app.core.config import settings

YANDEX_AUTH_URL = "https://oauth.yandex.ru/authorize"
YANDEX_TOKEN_URL = "https://oauth.yandex.ru/token"
YANDEX_USER_INFO_URL = "https://login.yandex.ru/info"


def get_yandex_oauth_url() -> str:
    return (
        f"{YANDEX_AUTH_URL}?response_type=code"
        f"&client_id={settings.YANDEX_CLIENT_ID}"
    )


async def exchange_code_for_token(code: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            YANDEX_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": settings.YANDEX_CLIENT_ID,
                "client_secret": settings.YANDEX_CLIENT_SECRET,
            },
        )
        return response.json()


async def get_yandex_user_info(access_token: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            YANDEX_USER_INFO_URL,
            headers={"Authorization": f"OAuth {access_token}"},
        )
        return response.json()
