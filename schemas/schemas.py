from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str
    avatar: Optional[str] = None
    bio: Optional[str] = None       

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    bio: Optional[str] = None


class ThreadBase(BaseModel):
    parent_thread_id: Optional[str] = None
    content: str

class ThreadCreate(ThreadBase):
    pass

class ThreadRead(ThreadCreate):
    thread_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ThreadUpdate(BaseModel):
    content: Optional[str]

class LikeCreate(BaseModel):
    thread_id: int

class LikeRead(LikeCreate):
    pass

class FollowerCreate(BaseModel):
    followed_id: int

class FollowerRead(FollowerCreate):
    pass

