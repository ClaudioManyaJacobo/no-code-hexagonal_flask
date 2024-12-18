from flask import render_template, request, redirect, url_for, session
from application.movie.movie_service import MovieService
from infrastructure.persistence.movie_api_repository import MovieApiRepository

# Configuración de la API
API_KEY = "e5d86b492f30d1b695069fefdfe9abd0"
movie_repository = MovieApiRepository(API_KEY)
movie_service = MovieService(movie_repository)

# Métodos de controlador para las películas
def index():
    # Verifica si el usuario ha iniciado sesión
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Si no está autenticado, redirige al login

    title = request.args.get('title', '')  # Obtener el título de la búsqueda
    genre_id = request.args.get('genre_id', '')  # Obtener el ID del género
    if title:
        # Llamar al servicio para buscar las películas por título
        movies = movie_service.index(title)
    elif genre_id:
        # Llamar al servicio para buscar las películas por género
        movies = movie_service.search_by_genre(genre_id)
    else:
        # Llamar al servicio para obtener las 10 películas populares
        movies = movie_service.index()
    return render_template("movie/index.html", movies=movies)


def show(movie_id):
    # Verifica si el usuario ha iniciado sesión
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Si no está autenticado, redirige al login

    # Asegúrate de que al acceder a los detalles de la película, uses 'movie_id'
    movie = movie_service.show(movie_id)
    return render_template('movie/show.html', movie=movie)
