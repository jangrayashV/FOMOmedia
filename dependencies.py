from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from sqlalchemy import select
from db import get_db
from utils.token_utils import verify_access_token
from models import User


OAuth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")

async def get_current_user(token: str = Depends(OAuth2_scheme), db:AsyncSession = Depends(get_db)):
    payload = verify_access_token(token)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    response = await db.execute(select(User).where(User.user_id == int(user_id)))
    current_user = response.scalar_one_or_none()

    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return current_user