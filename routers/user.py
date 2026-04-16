from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db import get_db
from schemas import UserUpdate, UserRead
from models import User, Follower
from dependencies import get_current_user   

router = APIRouter(prefix="/v1/user", tags=["user"])

@router.get("/{user_id}")
async def get_user_profile(user_id: int, db:AsyncSession=Depends(get_db), current_user:User=Depends(get_current_user)):
    response = await db.execute(select(User).where(User.user_id == user_id))
    existing_user = response.scalar_one_or_none()

    if not existing_user:
        raise HTTPException(status_code=404, detail="user doesn't exist")

    response = await db.execute(select(Follower).where(Follower.followed_id == user_id))
    followers = response.scalars().all()

    # return {"user": existing_user, "followers": followers}
    return {
        "user": {
            "user_id": existing_user.user_id,
            "email": existing_user.email,
            "username": existing_user.username,
            "avatar": existing_user.avatar,
            "bio": existing_user.bio,       
            "created_at": existing_user.created_at
        },
        "followers": [
            {
                "follower_id": follower.follower_id,
                "followed_id": follower.followed_id,
                "created_at": follower.created_at
            } for follower in followers

        ]
    }           

@router.patch("/update", response_model=UserRead)
async def update_user(user_update: UserUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    response = await db.execute(select(User).where(User.user_id == current_user.user_id))
    existing_user = response.scalar_one_or_none()

    if user_update.username:
        if user_update.username != existing_user.username:
            response = await db.execute(select(User).where(User.username == user_update.username))
            if response.scalar_one_or_none():
                raise HTTPException(status_code=400, detail="Username already taken")
            else:
                existing_user.username = user_update.username
    if user_update.password:
        from utils.auth_utils import hash_password
        existing_user.hashed_pwd = hash_password(user_update.password)
    if user_update.bio:
        existing_user.bio = user_update.bio 

    await db.commit()
    await db.refresh(existing_user)
    return existing_user    


@router.delete("/delete")
async def delete_user(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    response = await db.execute(select(User).where(User.user_id == current_user.user_id))
    existing_user = response.scalar_one_or_none()

    await db.delete(existing_user)
    await db.commit()
    return {"detail": "User deleted successfully"}