from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base
from datetime import datetime, UTC

class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    
    author = relationship("User", back_populates="posts")

    created_at = Column(DateTime, default=lambda: datetime.now(UTC))