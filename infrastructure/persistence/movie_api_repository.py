import requests
import yaml
import os
from domain.movie.movie_repository import MovieRepository
from domain.movie.movie import Movie
from typing import List
from urllib.parse import quote

class MovieApiRepository(MovieRepository):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.themoviedb.org/3/movie/popular"
        self.details_url = "https://api.themoviedb.org/3/movie"
        self.search_url = "https://api.themoviedb.org/3/search/movie"
        self.providers_url = "https://api.themoviedb.org/3/movie"
        
        self.platform_file = os.path.join(os.path.dirname(__file__), "platforms.yml")
        self.idioma_file = os.path.join(os.path.dirname(__file__), "idioma.yml")
        self.platform_urls = self.load_yaml(self.platform_file, "platforms")
        self.idiomas = self.load_yaml(self.idioma_file, "idiomas")

    
    # Cargar YAML de plataformas o idiomas
    def load_yaml(self, file_path: str, key: str):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
                return data.get(key, {})
        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"Error al leer el archivo {file_path}: {e}")
            return {}

    # Realizar solicitud a la API de manera segura
    def safe_request(self, url: str):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al hacer la solicitud: {e}")
            return None

    # Función para traducir el idioma
    def traducir_idioma(self, idioma_abrev):
        return self.idiomas.get(idioma_abrev, idioma_abrev)

    # Obtener actores de la película
    def get_actors(self, data):
        return [
            {"name": actor['name'], "photo": f"https://image.tmdb.org/t/p/w500{actor['profile_path']}"}
            for actor in data.get('credits', {}).get('cast', [])[:10]
            if actor.get('profile_path')
        ]

    # Crear la película con los datos obtenidos de la API
    def create_movie(self, data, platforms=None, actors=None, youtube_url=None, overview=None):
        director = next(
            (director['name'] for director in data.get('credits', {}).get('crew', []) if director['job'] == 'Director'),
            'Director no disponible'
        )
        return Movie(
            movie_id=data['id'],
            title=data['title'],
            release_date=data.get('release_date', 'Fecha no disponible'),
            poster_path=self.get_image_path(data.get('poster_path')),
            backdrop_path=self.get_image_path(data.get('backdrop_path'), is_backdrop=True),
            overview=overview or data.get('overview', 'Descripción no disponible'),
            genres=[{"id": genre['id'], "name": genre['name']} for genre in data.get('genres', [])],
            runtime=data.get('runtime'),
            tagline=data.get('tagline'),
            platforms=platforms or [],
            actors=actors or [],
            budget=data.get('budget'),
            revenue=data.get('revenue'),
            youtube_url=youtube_url,
            rating=data.get('vote_average'),
            original_language=self.traducir_idioma(data.get('original_language')),
            director=director
        )

    # Obtener la URL de la imagen (poster o backdrop)
    def get_image_path(self, path, is_backdrop=False):
        base_url = "https://image.tmdb.org/t/p/w500" if not is_backdrop else "https://image.tmdb.org/t/p/w1280"
        return f"{base_url}{path}" if path else None
    
# **********************************************************************************************
    # Obtener películas populares
    def index(self) -> List[Movie]:
        url = f"{self.base_url}?api_key={self.api_key}&language=es-MX"
        all_movies = []
        
        # Realizamos 3 solicitudes para obtener un total de 50 películas (3 páginas)
        for page in range(1, 4):  # Páginas 1, 2 y 3
            paginated_url = f"{url}&page={page}"
            data = self.safe_request(paginated_url)
            if data and data['total_results'] > 0:
                all_movies.extend([self.create_movie(item) for item in data['results']])
        
        # Limitamos a 50 si hay más resultados
        return all_movies[:50] if all_movies else []

    # Mostrar detalles de una película específica
    def show(self, movie_id: int, language='es-MX') -> Movie:
        data = self.fetch_movie_data(movie_id, language)
        if data:
            actors = self.get_actors(data)
            youtube_url = self.get_youtube_url(data)
            platforms = self.get_platforms(movie_id)
            overview = self.get_movie_overview(movie_id, language, data)
            return self.create_movie(data, platforms, actors, youtube_url, overview)
        return None
    
    # Metodo para buscar películas por género
    def search_by_genre(self, genre_id) -> List[Movie]:
        url = f"https://api.themoviedb.org/3/discover/movie?api_key={self.api_key}&with_genres={genre_id}&language=es-MX"
        all_movies = []
        
        # Realizamos 3 solicitudes para obtener un total de 50 películas (3 páginas)
        for page in range(1, 4):  # Páginas 1, 2 y 3
            paginated_url = f"{url}&page={page}"
            data = self.safe_request(paginated_url)
            if data and data['total_results'] > 0:
                all_movies.extend([self.create_movie(item) for item in data['results']])
        
        # Limitamos a 50 si hay más resultados
        return all_movies[:50] if all_movies else []
    
# *****************************************************************************************************************+   
    # Obtener la sinopsis de la película
    def get_movie_overview(self, movie_id, language, data):
        overview = data.get('overview')
        if not overview:
            # Fallback al inglés si no hay sinopsis en el idioma preferido
            fallback_data = self.safe_request(f"{self.details_url}/{movie_id}?api_key={self.api_key}&language=en-US&append_to_response=credits,videos")
            return fallback_data.get('overview', 'Descripción no disponible') if fallback_data else 'Descripción no disponible'
        return overview

    # Obtener el trailer de YouTube
    def get_youtube_url(self, data):
        return next(
            (f"https://www.youtube.com/watch?v={video['key']}" for video in data.get('videos', {}).get('results', []) if video['site'] == 'YouTube' and video['type'] == 'Trailer'),
            None
        )

    # Obtener las plataformas de streaming de la película
    def get_platforms(self, movie_id):
        providers_url = f"{self.providers_url}/{movie_id}/watch/providers?api_key={self.api_key}"
        providers_data = self.safe_request(providers_url)
        platforms_set = set()

        if providers_data and "results" in providers_data:
            for country_data in providers_data["results"].values():
                if "flatrate" in country_data:
                    for platform in country_data["flatrate"]:
                        platform_name = platform["provider_name"]
                        platform_logo = f"https://image.tmdb.org/t/p/w500{platform['logo_path']}" if platform.get("logo_path") else None
                        platform_url = self.platform_urls.get(platform_name)
                        if platform_url:
                            platforms_set.add((platform_name, platform_logo, platform_url))

        return [{"name": name, "logo": logo, "url": url} for name, logo, url in platforms_set]

    # Buscar películas por título
    def search(self, title: str) -> List[Movie]:
        url = f"{self.search_url}?api_key={self.api_key}&query={quote(title)}&language=es-ES"
        data = self.safe_request(url)
        return [self.create_movie(item) for item in data['results'][:20]] if data['total_results'] > 0 else []

    # Obtener los detalles completos de la película
    def fetch_movie_data(self, movie_id, language):
        url = f"{self.details_url}/{movie_id}?api_key={self.api_key}&language={language}&append_to_response=credits,videos"
        return self.safe_request(url)
   