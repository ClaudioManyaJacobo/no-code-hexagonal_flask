# domain/movie/movie.py
from typing import List, Dict

class Movie:
    def __init__(self, movie_id, title, release_date, poster_path, backdrop_path, 
                 overview, genres, runtime, tagline, platforms, actors, 
                 budget, revenue, youtube_url, rating=None, original_language=None, director=None):
        self.movie_id = movie_id
        self.title = title
        self.release_date = release_date
        self.poster_path = poster_path
        self.backdrop_path = backdrop_path 
        self.overview = overview
        self.genres = genres
        self.runtime = runtime
        self.tagline = tagline
        self.platforms = platforms
        self.actors = actors
        self.budget = budget
        self.revenue = revenue
        self.youtube_url = youtube_url
        self.rating = rating
        self.original_language = original_language
        self.director = director
