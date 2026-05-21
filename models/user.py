from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base
from datetime import datetime, UTC


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    bio = Column(String, nullable=True)

    posts = relationship("Post", back_populates="author")

    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
