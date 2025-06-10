# %%
from database import SessionLocal
from models import Movie, Rating, Tag, Link
db = SessionLocal()

# %%
movies = db.query(Movie).limit(10).all()

for movie in movies:
    if movie:
        print(movie.movieId, movie.title, movie.genres)
    else:
        print("aucun film trouvé")
# %%
action_movies = db.query(Movie).filter(Movie.genres.contains("Action")).limit(10)

for action_mov in action_movies:
    if action_mov:
        print(f"ID: {action_mov.movieId}, Title: {action_mov.title}, Genre: {action_mov.genres}")
    else:
        print("Pas de film d'action")
# %%
ratings = db.query(Rating).limit(10)

for rating in ratings:
    if rating:
        print(f"ID: {rating.movieId}, Rating: {rating.rating}")
    else:
        print("pas de note")
# %%
hight_rating_movie = (
                    db.query(Movie.title, Rating.rating)
                    .join(Rating)
                    .filter(Rating.rating>= 4, Movie.movieId==Rating.movieId)
                    .limit(10)
                    
)

for hrm in hight_rating_movie:
    if hrm:
        print(hrm)
    else:
        print("Introuvé")
# %%
tags = db.query(Tag).limit(5).all()

for tag in tags:
    print(f"userId: {tag.userId}, movieId: {tag.movieId}")
# %%
links = db.query(Link).limit(10)

for link in links:
    print(f"{link.imdbId}, {link.tmdbId}, {link.movieId}")
# %%
db.close()
# %%
