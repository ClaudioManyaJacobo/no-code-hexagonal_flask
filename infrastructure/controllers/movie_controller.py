from flask import render_template, request, redirect, url_for, session
from application.movie.movie_service import MovieService
from application.comment.comment_service import CommentService

class MovieController:
    def __init__(self, movie_service: MovieService, comment_service: CommentService):
        self.movie_service = movie_service
        self.comment_service = comment_service

    def index(self):
        if 'user_id' not in session:
            return redirect(url_for('user.login'))

        title = request.args.get('title', '')
        genre_id = request.args.get('genre_id', '')
        actor_name = request.args.get('actor_name', '')
        year = request.args.get('year', '')

        try:
            if title:
                movies = self.movie_service.index(title)
            elif genre_id:
                movies = self.movie_service.search_by_genre(genre_id)
            elif actor_name:
                movies = self.movie_service.search_by_actor(actor_name)
            elif year:
                movies = self.movie_service.search_by_year(year)
            else:
                movies = self.movie_service.index()

            return render_template("movie/index.html", movies=movies)

        except ValueError as e:
            return render_template("movie/index.html", movies=[], error=str(e))

    def show(self, movie_id):
        if 'user_id' not in session:
            return redirect(url_for('user.login'))

        movie = self.movie_service.show(movie_id)
        comments = self.comment_service.get_movie_comments(movie_id)

        if request.method == 'POST':
            content = request.form.get('comment')
            if content:
                try:
                    self.comment_service.add_comment(session['user_id'], movie_id, content)
                    return redirect(url_for('movie.show', movie_id=movie_id))
                except ValueError as e:
                    return render_template('movie/show.html', movie=movie, comments=comments, error=str(e))

        return render_template('movie/show.html', movie=movie, comments=comments)
