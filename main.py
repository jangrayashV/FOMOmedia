from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy import text
from core.db import engine

@asynccontextmanager
async def lifespan(app: FastAPI):

    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))

        print("Database connected")

    except Exception as e:
        print("Database connection failed:", e)

    yield

    await engine.dispose()

    print("Database disconnected")

app = FastAPI() 

@app.get("/")
def ping():
    return {"message": "pong!"}