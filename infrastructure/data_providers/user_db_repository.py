from domain.user.user import User
from domain.user.user_repository import UserRepository
from infrastructure.db.connection import Session

class UserApiRepository(UserRepository):
    def __init__(self):
        self.session = Session()

    def get_user_by_email(self, email: str):
        return self.session.query(User).filter_by(email=email).first()

    def create_user(self, name: str, email: str, password: str) -> User:
        new_user = User(name=name, email=email, password=password)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def update_user(self, user_id: int, name: str, password: str) -> None:
        user = self.session.query(User).filter_by(user_id=user_id).first()
        if user:
            user.name = name
            user.password = password
            self.session.commit()

    def get_user_by_id(self, user_id: int) -> User:
        return self.session.query(User).filter_by(user_id=user_id).first()
