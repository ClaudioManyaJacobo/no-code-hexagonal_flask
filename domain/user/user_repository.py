from abc import ABC, abstractmethod
from domain.user.user import User

# Interfaz que define los métodos que debe implementar un repositorio de usuarios
class UserRepository(ABC):
    # Método para obtener un usuario por su ID
    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        pass
    
    # Método para obtener un usuario por su email
    @abstractmethod
    def create_user(self, user: User) -> User:
        pass
    