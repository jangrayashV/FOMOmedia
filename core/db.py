from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from core.config import settings

DATABASE_URL = settings.DATABASE_URL

# Engine — created once at startup
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  
)

# Base for all models
class Base(DeclarativeBase):
    pass


# Dependency — yields a session per request, auto-closes on exit
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session