from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager
from db import engine, Base
from routers import auth, pov, user, like, follow




@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    return {"message": "wsup gaaaaang!"}

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(pov.router)
app.include_router(like.router)
app.include_router(follow.router)