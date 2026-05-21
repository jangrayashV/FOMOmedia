from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base
from datetime import datetime, UTC

class Like(Base):
    __tablename__ = "likes"

    like_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    author = relationship("User", back_populates="comments")
    
    post_id = Column(Integer, ForeignKey("posts.post_id"), nullable=False)
    post = relationship("Post", back_populates="comments")

    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
