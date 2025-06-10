from database import SessionLocal
from query_helpers import *

db= SessionLocal()

movie = get_movie(db, movie_id=1)
# print(movie.title, movie.genres)
db.close()

movies = get_movies(db, limit=5)
# for film in movies:
#     print(f"title: {film.title}, genre: {film.genres}")

rating = get_rating(db, user_id=5, movie_id=1)
# print(rating.movieId, rating.rating)

ratings = get_ratings(db, limit=10, user_id= 5)
# for note in ratings:
#     print(f"user_id: {note.userId}, ID: {note.movieId}, Rating: {note.rating}")

tag = get_tag(db, movie_id=60756, user_id=2, tag_text="funny")
# print(f"movie_id: {tag.movieId}, movie_tag: {tag.tag} ")

tags = get_tags(db, limit=10, movie_id=1569)
for tag in tags:
    if tag:
        print(f"user_id: {tag.userId}, movie_id: {tag.movieId}, tag: {tag.tag}")
    else:
        pass
