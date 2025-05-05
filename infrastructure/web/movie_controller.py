# infrastructure/web/movie_controller.py
from flask import render_template, request, redirect, url_for, session
from application.movie.movie_service import MovieService
from application.comment.comment_service import CommentService
from infrastructure.persistence.movie_api_repository import MovieApiRepository
from infrastructure.persistence.comment_db_repository import CommentDbRepository

# Configuración de la API
API_KEY = "e5d86b492f30d1b695069fefdfe9abd0"
movie_repository = MovieApiRepository(API_KEY)
movie_service = MovieService(movie_repository)
comment_repository = CommentDbRepository()
comment_service = CommentService(comment_repository)

def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    title = request.args.get('title', '')
    genre_id = request.args.get('genre_id', '')
    if title:
        movies = movie_service.index(title)
    elif genre_id:
        movies = movie_service.search_by_genre(genre_id)
    else:
        movies = movie_service.index()
    return render_template("movie/index.html", movies=movies)

def show(movie_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Obtener la película
    movie = movie_service.show(movie_id)
    
    # Obtener comentarios
    comments = comment_service.get_movie_comments(movie_id)
    
    # Manejar envío de nuevo comentario (solo si es POST)
    if request.method == 'POST':
        content = request.form.get('comment')
        if content:
            try:
                comment_service.add_comment(session['user_id'], movie_id, content)
                return redirect(url_for('show', movie_id=movie_id))
            except ValueError as e:
                # Manejar error de validación (comentario vacío)
                return render_template(
                    'movie/show.html', 
                    movie=movie, 
                    comments=comments,
                    error=str(e)
                )
    
    # Si es GET o después de manejar POST sin redirección
    return render_template('movie/show.html', movie=movie, comments=comments)