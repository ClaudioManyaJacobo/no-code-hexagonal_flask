# application/comment/comment_service.py
from domain.comment.comment_repository import CommentRepository
from domain.comment.comment import Comment
from typing import List

class CommentService:
    def __init__(self, repository: CommentRepository):
        self.repository = repository
    
    def add_comment(self, user_id: int, movie_id: int, content: str) -> Comment:
        if not content or len(content.strip()) == 0:
            raise ValueError("El comentario no puede estar vacío")
        return self.repository.create(user_id, movie_id, content)
    
    def get_movie_comments(self, movie_id: int) -> List[Comment]:
        return self.repository.get_by_movie(movie_id)
    
    def get_user_comments(self, user_id: int) -> List[Comment]:
        return self.repository.get_by_user(user_id)
    
    def delete_comment(self, comment_id: int, user_id: int) -> bool:
        return self.repository.delete(comment_id, user_id)