from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from infrastructure.db.base import Base

class Comment(Base):
    __tablename__ = 'comments'

    comment_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    movie_id = Column(Integer)
    content = Column(String)
    created_at = Column(DateTime)
