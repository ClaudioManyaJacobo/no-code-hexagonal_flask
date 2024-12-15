from flask import Flask, render_template, request
from infrastructure.persistence.movie_api_repository import MovieApiRepository
from application.movie.movie_service import MovieService

app = Flask(__name__, 
            template_folder='C:/Users/claud/Downloads/REFACT_PYTHON/templates',
            static_folder='C:/Users/claud/Downloads/REFACT_PYTHON/static')

# Configuración de la API
API_KEY = "e5d86b492f30d1b695069fefdfe9abd0"
# Inicializamos el repositorio y el servicio
movie_repository = MovieApiRepository(API_KEY)
movie_service = MovieService(movie_repository)

@app.route('/')
def index():
    title = request.args.get('title', '')  # Obtener el título de la búsqueda
    if title:
        # Llamar al servicio para buscar las películas por título
        movies = movie_service.index(title)
    else:
        # Llamar al servicio para obtener las 10 películas populares
        movies = movie_service.index()
    return render_template("movie/index.html", movies=movies)

@app.route('/movie/<int:movie_id>')
def show(movie_id):
    # Asegúrate de que al acceder a los detalles de la película, uses 'movie_id'
    movie = movie_service.show(movie_id)
    return render_template('movie/show.html', movie=movie)
