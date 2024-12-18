# user_service.py
from werkzeug.security import generate_password_hash, check_password_hash
from domain.user.user import User
from domain.user.user_repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    # Métodos de servicio para el usuario
    # Método para autenticar un usuario
    def authenticate_user(self, email, password):
        user = self.user_repository.get_user_by_email(email)
        if user and check_password_hash(user.password, password):  
            return user
        return None
    
    # Método para crear un usuario
    def create_user(self, name, email, password):
        hashed_password = generate_password_hash(password)  
        return self.user_repository.create_user(name, email, hashed_password)

    # Método para actualizar un usuario
    def update_user(self, user_id, name, password):
        hashed_password = generate_password_hash(password)
        self.user_repository.update_user(user_id, name, hashed_password)

    # Métodos para obtener un usuario (email)
    def get_user_by_email(self, email):
        return self.user_repository.get_user_by_email(email)

    # Método para obtener un usuario (id)
    def get_user_by_id(self, user_id):
        return self.user_repository.get_user_by_id(user_id)
