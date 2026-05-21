from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base
from datetime import datetime, UTC

class Comment(Base):
    __tablename__ = "comments"

    parent_comment_id = Column(Integer, ForeignKey("comments.comment_id"), nullable=True)
    comment_id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    author = relationship("User", back_populates="comments")

    post_id = Column(Integer, ForeignKey("posts.post_id"), nullable=False)
    post = relationship("Post", back_populates="comments")

    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
