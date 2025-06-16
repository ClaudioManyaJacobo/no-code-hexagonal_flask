from sqlalchemy.orm import Session
from domain.comment.comment_repository import CommentRepository
from domain.comment.comment import Comment
from infrastructure.db.connection import Session as DBSession
from typing import List
from datetime import datetime

class CommentDbRepository(CommentRepository):
    def __init__(self):
        self.session: Session = DBSession()

    def create(self, user_id: int, movie_id: int, content: str) -> Comment:
        comment = Comment(user_id=user_id, movie_id=movie_id, content=content, created_at=datetime.now())
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)  # para obtener el ID generado
        return comment

    def get_by_movie(self, movie_id: int) -> List[Comment]:
        return self.session.query(Comment)\
            .filter(Comment.movie_id == movie_id)\
            .order_by(Comment.created_at.desc())\
            .all()

    def get_by_user(self, user_id: int) -> List[Comment]:
        return self.session.query(Comment)\
            .filter(Comment.user_id == user_id)\
            .order_by(Comment.created_at.desc())\
            .all()

    def delete(self, comment_id: int, user_id: int) -> bool:
        result = self.session.query(Comment)\
            .filter(Comment.comment_id == comment_id, Comment.user_id == user_id)\
            .delete()
        self.session.commit()
        return result > 0
