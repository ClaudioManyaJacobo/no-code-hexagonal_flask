from abc import ABC, abstractmethod
from .user import User

class UserRepository(ABC):
    # Metodo para obtener el email del usuario
    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        pass
    
    # Metodo para crear un usuario
    @abstractmethod
    def create_user(self, name: str, email: str, password: str) -> User:
        pass
    
    # Metodo para actualizar un usuario
    @abstractmethod
    def update_user(self, user_id: int, name: str, password: str) -> None:
        pass  
    
    # Metodo para obtener un usuario por su ID
    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        pass