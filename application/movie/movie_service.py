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
    
    # clase search_by_genre para buscar películas por género
    def search_by_genre(self, genre_id: str) -> List[Movie]:
        return self.repository.search_by_genre(genre_id)
    
        # Nuevo método para buscar por actor
    def search_by_actor(self, actor_name: str) -> List[Movie]:
        if not actor_name:
            return []
        return self.repository.search_by_actor(actor_name)
    
    # Nuevo método para buscar por año
    def search_by_year(self, year: int) -> List[Movie]:
        try:
            year_int = int(year)
            if year_int < 1900 or year_int > 2100:
                return []
            return self.repository.search_by_year(year_int)
        except (ValueError, TypeError):
            return []
