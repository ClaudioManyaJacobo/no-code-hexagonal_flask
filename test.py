import requests

API_KEY = 'e5d86b492f30d1b695069fefdfe9abd0'
MOVIE_ID = 40697
BASE_URL = "https://api.themoviedb.org/3/movie"
LANGUAGES = ['en', 'es-MX', 'fr', 'de', 'it', 'pt']

def safe_request(url: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud: {e}")
        return None

def get_movie_details(movie_id):
    # Intentamos obtener los detalles de la película en varios idiomas
    for language in LANGUAGES:
        url = f"{BASE_URL}/{movie_id}?api_key={API_KEY}&language={language}&append_to_response=credits,videos"
        data = safe_request(url)
        if data and data.get('overview'):
            return data
    # Si no encontramos la sinopsis en ninguno de los idiomas, devolvemos None
    return None

def display_movie_info(movie_id):
    movie_data = get_movie_details(movie_id)
    if movie_data:
        print(f"Title: {movie_data['title']}")
        print(f"Release Date: {movie_data.get('release_date', 'Fecha no disponible')}")
        print(f"Overview: {movie_data.get('overview', 'Sinopsis no disponible')}")
        print(f"Genres: {[genre['name'] for genre in movie_data.get('genres', [])]}")
        print(f"Director: {next((director['name'] for director in movie_data.get('credits', {}).get('crew', []) if director['job'] == 'Director'), 'Director no disponible')}")
        print(f"Rating: {movie_data.get('vote_average', 'No disponible')}")
        print(f"Original Language: {movie_data.get('original_language', 'No disponible')}")
        print(f"Poster Path: {movie_data.get('poster_path', 'No disponible')}")
        print(f"Backdrop Path: {movie_data.get('backdrop_path', 'No disponible')}")
        
        # Mostrar los actores
        print("Actors:")
        for actor in movie_data.get('credits', {}).get('cast', [])[:5]:  # Limitar a los primeros 5 actores
            print(f"- {actor['name']}")

    else:
        print(f"No se encontraron detalles para la película con ID {movie_id}.")

if __name__ == "__main__":
    display_movie_info(MOVIE_ID)
