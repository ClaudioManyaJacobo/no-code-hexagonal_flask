# domain/comment/comment_repository.py
from abc import ABC, abstractmethod
from .comment import Comment
from typing import List

class CommentRepository(ABC):
    @abstractmethod
    def create(self, user_id: int, movie_id: int, content: str) -> Comment:
        pass
    
    @abstractmethod
    def get_by_movie(self, movie_id: int) -> List[Comment]:
        pass
    
    @abstractmethod
    def get_by_user(self, user_id: int) -> List[Comment]:
        pass
    
    @abstractmethod
    def delete(self, comment_id: int, user_id: int) -> bool:
        pass