from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db import get_db
from schemas import LikeCreate
from models import Like, User
from dependencies import get_current_user


router = APIRouter(prefix="/likes", tags=["likes"])
@router.post("/")
async def create_like(like: LikeCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    response = await db.execute(select(Like).where(Like.user_id == current_user.user_id, Like.pov_id == like.pov_id))
    existing_like_by_user = response.scalar_one_or_none()
    if existing_like_by_user:
        await db.delete(existing_like_by_user)
        await db.commit()
        return {"message": "unliked"}
    else:
        new_like = Like(user_id=current_user.user_id, pov_id=like.pov_id)
        db.add(new_like)
        await db.commit()
        await db.refresh(new_like)
        return {"message": "liked"}