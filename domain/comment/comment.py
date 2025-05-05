# domain/comment/comment.py
class Comment:
    def __init__(self, comment_id: int, user_id: int, movie_id: int, content: str, created_at: str):
        self.comment_id = comment_id
        self.user_id = user_id
        self.movie_id = movie_id
        self.content = content
        self.created_at = created_at