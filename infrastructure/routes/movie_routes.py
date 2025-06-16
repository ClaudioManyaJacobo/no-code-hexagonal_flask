from flask import Blueprint
from infrastructure.controllers.movie_controller import MovieController
from application.movie.movie_service import MovieService
from application.comment.comment_service import CommentService
from infrastructure.data_providers.movie_api_repository import MovieApiRepository
from infrastructure.data_providers.comment_db_repository import CommentDbRepository

movie_bp = Blueprint('movie', __name__)
movie_service = MovieService(MovieApiRepository("e5d86b492f30d1b695069fefdfe9abd0"))
comment_service = CommentService(CommentDbRepository())
controller = MovieController(movie_service, comment_service)

movie_bp.route('/', methods=['GET'])(controller.index)
movie_bp.route('/movie/<int:movie_id>', methods=['GET', 'POST'])(controller.show)
