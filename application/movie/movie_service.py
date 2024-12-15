# application/movie_service.py
from domain.movie.movie_repository import MovieRepository
from domain.movie.movie import Movie
from typing import List

class MovieService:
    def __init__(self, repository: MovieRepository):
        self.repository = repository

    # Clase index para realizar busqueda y mostrar las películas
    def index(self, title: str = '') -> List[Movie]:
        if title:
            return self.repository.search(title)
        else:
            return self.repository.index()
    
    # Clase show para mostrar los detalles de una película
    def show(self, movie_id: int) -> Movie:
        return self.repository.show(movie_id)
