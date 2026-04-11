from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, DateTime
from db import Base
from datetime import datetime, timezone


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String, nullable=False)
    hashed_pwd = Column(String)
    avatar = Column(String)
    bio = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class Thread(Base):
    __tablename__ = "threads"

    thread_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    parent_thread_id = Column(Integer, ForeignKey("threads.thread_id"), nullable=True)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class Like(Base):
    __tablename__ = "likes"
    __table_args__ = (UniqueConstraint("user_id", "thread_id"),)

    liked_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    thread_id = Column(Integer, ForeignKey("threads.thread_id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class Follower(Base):
    __tablename__ = "followers"
    # redundant unique constraint, but it is here for clarity and to ensure that the combination of follower_id and followed_id is unique
    # __table_args__ = (UniqueConstraint("follower_id", "followed_id"), )

    follower_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    followed_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)