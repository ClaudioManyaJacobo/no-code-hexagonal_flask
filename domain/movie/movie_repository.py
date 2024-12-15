# domain/movie_repository.py
from abc import ABC, abstractmethod
from typing import List
from domain.movie.movie import Movie

class MovieRepository(ABC):
    # Método index para retornar una lista de películas (Methodabstract)
    @abstractmethod
    def index (self, title: str) -> List[Movie]:
        pass
    
    # Método show para mostrar los detalles de una película (Methodabstract)
    @abstractmethod
    def show(self, movie_id: int) -> Movie:
        pass