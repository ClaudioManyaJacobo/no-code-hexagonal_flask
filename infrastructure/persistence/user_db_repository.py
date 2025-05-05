# infrastructure/persistence/user_api_repository.py
from domain.user.user import User
from domain.user.user_repository import UserRepository
from infrastructure.db.connection import get_connection

class UserApiRepository(UserRepository):
    def __init__(self):
        self.connection = get_connection()
        self.cursor = self.connection.cursor()

    def get_user_by_email(self, email: str) -> User:
        self.cursor.execute("SELECT user_id, name, email, password FROM users WHERE email = %s", (email,))
        row = self.cursor.fetchone()
        if row:
            return User(row[0], row[1], row[2], row[3])
        return None

    def create_user(self, name: str, email: str, password: str) -> User:
        self.cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        self.connection.commit()
        self.cursor.execute("SELECT @@IDENTITY")
        user_id = self.cursor.fetchone()[0]
        return User(user_id, name, email, password)

    def update_user(self, user_id: int, name: str, password: str) -> None:
        self.cursor.execute("UPDATE users SET name = %s, password = %s WHERE user_id = %s", (name, password, user_id))
        self.connection.commit()

    def get_user_by_id(self, user_id: int) -> User:
        self.cursor.execute("SELECT user_id, name, email, password FROM users WHERE user_id = %s", (user_id,))
        row = self.cursor.fetchone()
        if row:
            return User(row[0], row[1], row[2], row[3])
        return None
