from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from sqlalchemy.orm import declarative_base

Base = declarative_base()

engine = create_async_engine(settings.DATABASE_URL, echo=True)

async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def get_db():
    async with async_session() as session:
        yield session
