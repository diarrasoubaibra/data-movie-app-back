from fastapi import Depends, FastAPI, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from database import SessionLocal
import query_helpers as helpers
import schemas

api_description ="""
Bienvenue dans l'API MovieLens

Cette API permet d'interagir avec une base de données inspirée du célèbre jeu de données [MovieLens](https://grouplens.org/datasets/movielens/).  
Elle est idéale pour découvrir comment consommer une API REST avec des données de films, d'utilisateurs, d'évaluations, de tags et de liens externes (IMDB, TMDB).

### Fonctionnalités disponibles :

- Rechercher un film par ID, ou lister tous les films
- Consulter les évaluations (ratings) par utilisateur et/ou film
- Accéder aux tags appliqués par les utilisateurs sur les films
- Obtenir les liens IMDB / TMDB pour un film
- Voir des statistiques globales sur la base

Tous les endpoints supportent la pagination (`skip`, `limit`) et des filtres optionnels selon les cas.

### Bon à savoir
- Vous pouvez tester tous les endpoints directement via l'interface Swagger "/docs".
- Pour toute erreur (ex : ID inexistant), une réponse claire est retournée avec le bon code HTTP.
"""

app = FastAPI(
    title="MoviesLens API",
    description = api_description,
    version = "0.1"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get(
    "/",
    summary="vérification de la santé de l'api",
    description=" Vérifie que l'api fonction correctement",
    response_description="statut de l'api",
    operation_id="health_check_movies_api",
    tags=["monitoring"]
)

async def root():
    return {"message": "API MovieLens Opérationnelle"}

# Endpoint pour obtenir les films
@app.get(
    "/movies/{movie_id}",
    summary="Obtenir un film par son ID",
    description="Retourne les informations d'un film vi son ID",
    response_description="Détails du film",
    response_model=schemas.MovieDetailed,
    tags=["films"],
)
def read_movie(movie_id: int = Path(..., description="identifiant unique du film"), db: Session = Depends(get_db)):
    movie = helpers.get_movie(db, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail=f"Film avec l'ID {movie_id} non trouvé")
    return movie
@app.get(
    "/movies",
    summary="Lister les films",
    description="Retourne une liste de film avec pagination et filtre optionnels par titre ou genre.",
    response_description="Liste de film",
    response_model=List[schemas.MovieSimple],
    tags=["films"],
)
def list_movies(
    skip: int = Query(0, ge=0, description="Nombre de résultats à ignorer"),
    limit: int = Query(100, le=1000, description="Nombre maximal de résultats à retourner"),
    title: str = Query(None, description="Filtre par titre"),
    genre: str = Query(None, description="Filtre par genre"),
    db: Session = Depends(get_db)
):
    movies = helpers.get_movies(db, skip=skip, limit=limit, title=title, genre=genre)
    return movies


# Obtenir l'évaluation d'utilisateur pour un film
@app.get(
    "/rating/{user_id}/{movie_id}",
    summary="Obtenir l'évaluation d'un utilisateur sur un film",
    description="Retourne l'évalutaion d'un utilisateur pour sur film",
    response_description="Détails de l'évaluation",
    response_model=schemas.RatingBase,
    tags=["Evaluations"],
)
def read_rating(
    user_id: int = Path(..., description="identifiant unique de l'utilisateur"),
    movie_id: int = Path(..., description="identifiant unique du film"),
    db: Session = Depends(get_db)
):
    rating = helpers.get_rating(db, user_id, movie_id)
    if rating is None:
        raise HTTPException(status_code=404, detail=f"Aucune évalutaion trouvé pour l'utilisateur {user_id} pour le Film avec l'ID {movie_id}")
    return rating

@app.get(
    "/ratings",
    summary="Lister les évaluations d'un films",
    description="Retourne une liste des évaluations d'un film",
    response_description="Liste des évaluations",
    response_model=List[schemas.RatingSimple],
    tags=["Evaluations"],
)
def list_ratings(
    skip: int = Query(0, ge=0, description="Nombre de résultats à ignorer"),
    limit: int = Query(100, le=1000, description="Nombre maximal de résultats à retourner"),
    movie_id: Optional[int] = Query(None, description="l'identifiant du film"),
    user_id: Optional[int] = Query(None, description="ID de l'utilisateur"),
    min_rating: Optional[float] = Query(None, description="Note minimale"),
    db: Session = Depends(get_db)
):
    ratings = helpers.get_ratings(db, skip=skip, limit=limit, movie_id=movie_id, user_id=user_id, min_rating=min_rating)
    return ratings

# obtenir les tags
@app.get(
    "/tag/{user_id}/{movie_id}/{tag_text}",
    summary="Obtenir le tag d'un utilisateur sur un film",
    description="Retourne le tag d'un utilisateur pour sur film",
    response_description="Détails du tag",
    response_model=schemas.TagSimple,
    tags=["Tags"],
)
def read_tag(
    user_id: int = Path(..., description="identifiant unique de l'utilisateur"),
    movie_id: int = Path(..., description="identifiant unique du film"),
    tag_text: str = Path(..., description="le tag"),
    db: Session = Depends(get_db)
):
    tag = helpers.get_tag(db, user_id, movie_id, tag_text)
    if tag is None:
        raise HTTPException(status_code=404, detail=f"Aucun tag trouvé pour l'utilisateur {user_id} pour le Film avec l'ID {movie_id}")
    return tag

@app.get(
    "/tags",
    summary="Obtenir le tag d'un utilisateur sur un film",
    description="Retourne le tag d'un utilisateur pour sur film",
    response_description="Détails du tag",
    response_model=List[schemas.TagSimple],
    tags=["Tags"],
)
def list_tags(
    skip: int = Query(0, ge=0, description="Nombre de résultats à ignorer"),
    limit: int = Query(100, le=1000, description="Nombre maximal de résultats à retourner"),
    movie_id: Optional[int] = Query(None, description="l'identifiant du film"),
    user_id: Optional[int] = Query(None, description="ID de l'utilisateur"),
    db: Session = Depends(get_db)
):
    tags = helpers.get_tags(db, skip=skip, limit=limit, movie_id=movie_id, user_id=user_id)
    return tags

# Obtenir les links
@app.get(
    "/link/{movie_id}",
    summary="Obtenir le tag d'un utilisateur sur un film",
    description="Retourne le tag d'un utilisateur pour sur film",
    response_description="Détails du tag",
    response_model=schemas.LinkSimple,
    tags=["Links"],
)
def read_link(
    movie_id: int = Path(..., description="identifiant unique du film"),
    db: Session = Depends(get_db)
):
    link = helpers.get_link(db,  movie_id)
    if link is None:
        raise HTTPException(status_code=404, detail=f"Aucun lien trouvé pour l'utilisateur {user_id} pour le Film avec l'ID {movie_id}")
    return link

@app.get(
    "/links",
    summary="Lister les liens des films",
    description="Retourne une liste paginée des identifiants IMDB et TMDB de tous les film",
    response_description="Détails des liens",
    response_model=List[schemas.LinkSimple],
    tags=["Links"],
)
def list_links(
    skip: int = Query(0, ge=0, description="Nombre de résultats à ignorer"),
    limit: int = Query(100, le=1000, description="Nombre maximal de résultats à retourner"),
    db: Session = Depends(get_db)
):
    links = helpers.get_links(db, skip=skip, limit=limit)
    return links


# Obtenir les statistiques sur la db
@app.get(
    "/analystics",
    summary="Obtenir des statistiques",
    description="""
    Retourne un résumé analytique de la db

    - Nombre total de films
    - Nombre total d'évaluation
    - Nombre total de tags
    - Nombre total de liens IMDB/TMDB
    """,
    response_model=schemas.AnalyticsResponse,
    tags=["Analytics"]
)
def get_analytics(db: Session=Depends(get_db)):
    movie_count = helpers.get_movie_count(db)
    rating_count = helpers.get_rating_count(db)
    tag_count = helpers.get_rating_count(db)
    link_count = helpers.get_link_count(db)

    return schemas.AnalyticsResponse(
        movie_count=movie_count,
        rating_count=rating_count,
        tag_count=tag_count,
        link_count=link_count
    )