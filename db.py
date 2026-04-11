from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import Settings


SQLALCHEMY_DATABASE_URI = Settings().SQLALCHEMY_DATABASE_URI

engine = create_async_engine(SQLALCHEMY_DATABASE_URI, echo=True)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

async def get_db():
    db_session = AsyncSessionLocal()
    try:
        yield db_session
    finally:
        db_session.close() 