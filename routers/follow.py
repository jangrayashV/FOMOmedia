from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db import get_db
from models import Follower, User
from dependencies import get_current_user


router = APIRouter(prefix="/follow", tags=["follow"])

@router.post("/{user_id}")
async def follow_user(user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if user_id == current_user.user_id:
        raise HTTPException(status_code=400, detail="you can't follow yourself")

    response = await db.execute(select(Follower).where(Follower.follower_id == current_user.user_id, Follower.followed_id == user_id))
    existing_relation = response.scalar_one_or_none()

    if existing_relation:
        await db.delete(existing_relation)
        await db.commit()
        return {"message": "unfollowed"}
    else:
        new_relation = Follower(
            follower_id = current_user.user_id,
            followed_id = user_id
        )
        db.add(new_relation)
        await db.commit()
        await db.refresh(new_relation)
        return {"message": "followed"}