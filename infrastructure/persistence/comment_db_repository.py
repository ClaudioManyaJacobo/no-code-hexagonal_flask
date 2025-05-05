# infrastructure/persistence/comment_db_repository.py
from domain.comment.comment_repository import CommentRepository
from domain.comment.comment import Comment
from typing import List
from datetime import datetime
from infrastructure.db.connection import get_connection

class CommentDbRepository(CommentRepository):
    def __init__(self):
        self.connection = get_connection()
    
    def create(self, user_id: int, movie_id: int, content: str) -> Comment:
        cursor = self.connection.cursor()
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            "INSERT INTO comments (user_id, movie_id, content, created_at) VALUES (%s, %s, %s, %s)",
            (user_id, movie_id, content, created_at)
        )
        self.connection.commit()
        comment_id = cursor.lastrowid
        return Comment(comment_id, user_id, movie_id, content, created_at)
    
    def get_by_movie(self, movie_id: int) -> List[Comment]:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT comment_id, user_id, movie_id, content, created_at FROM comments WHERE movie_id = %s ORDER BY created_at DESC",
            (movie_id,)
        )
        return [
            Comment(row[0], row[1], row[2], row[3], row[4])
            for row in cursor.fetchall()
        ]
    
    def get_by_user(self, user_id: int) -> List[Comment]:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT comment_id, user_id, movie_id, content, created_at FROM comments WHERE user_id = %s ORDER BY created_at DESC",
            (user_id,)
        )
        return [
            Comment(row[0], row[1], row[2], row[3], row[4])
            for row in cursor.fetchall()
        ]
    
    def delete(self, comment_id: int, user_id: int) -> bool:
        cursor = self.connection.cursor()
        cursor.execute(
            "DELETE FROM comments WHERE comment_id = %s AND user_id = %s",
            (comment_id, user_id)
        )
        self.connection.commit()
        return cursor.rowcount > 0