import random
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Movie, TVShow, AnimationMovie
from database import get_db
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/random/movie")
def get_random_movie(db: Session = Depends(get_db)):
    movies = db.query(Movie).all()
    if not movies:
        return {"message": "Nav pieejamu filmu"}
    random_movie = random.choice(movies)
    return {
        "title": random_movie.title,
        "poster": random_movie.poster_url,
        "rating": random_movie.rating
    }

@router.get("/random/tvshow")
def get_random_tvshow(db: Session = Depends(get_db)):
    shows = db.query(TVShow).all()
    if not shows:
        return {"message": "Nav pieejamu seriālu"}
    random_show = random.choice(shows)
    return {
        "title": random_show.title,
        "poster": random_show.poster_url,
        "rating": random_show.rating
    }

@router.get("/random/animation")
def get_random_animation(db: Session = Depends(get_db)):
    animations = db.query(AnimationMovie).all()
    if not animations:
        return {"message": "Nav pieejamu animācijas filmu"}
    random_animation = random.choice(animations)
    return {
        "title": random_animation.title,
        "poster": random_animation.poster_url,
        "rating": random_animation.rating
    }
