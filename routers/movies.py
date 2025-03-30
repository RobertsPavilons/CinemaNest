from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from database import get_db
from models import Movie, Actor
from routers.schemas import MovieCreate, MovieResponse, MovieUpdate, ActorCreate, ActorResponse
from routers.auth import get_admin_user
from typing import List
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/movielist")
def movies_page(request: Request):
    return templates.TemplateResponse("movies.html", {"request": request})

@router.get("/movies", response_model=List[MovieResponse])
def get_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()

@router.get("/movies/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.get("/movielist/{id}")
def movie_details(id: int, request: Request, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Filma nav atrasta")

    return templates.TemplateResponse("movie.html", {
        "request": request,
        "movie": movie
    })

@router.post("/movies", response_model=MovieResponse)
def add_movie(
    movie: MovieCreate, 
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_admin_user)
):
    new_movie = Movie(
        title=movie.title,
        description=movie.description,
        year=movie.year,
        poster_url=movie.poster_url,
        trailer_url=movie.trailer_url,
        category=movie.category,
        rating=movie.rating
    )
    if movie.actors:
        actors = db.query(Actor).filter(Actor.id.in_(movie.actors)).all()
        new_movie.actors = actors

    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie

@router.put("/movies/{movie_id}", response_model=MovieResponse)
def update_movie(
    movie_id: int, 
    movie_update: MovieUpdate, 
    db: Session = Depends(get_db), 
    current_admin: str = Depends(get_admin_user)  
):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    updated_fields = []
    if movie_update.title:
        movie.title = movie_update.title
        updated_fields.append("title")
    if movie_update.description:
        movie.description = movie_update.description
        updated_fields.append("description")
    if movie_update.year:
        movie.year = movie_update.year
        updated_fields.append("year")
    if movie_update.poster_url:
        movie.poster_url = movie_update.poster_url
        updated_fields.append("poster_url")
    if movie_update.trailer_url:
        movie.trailer_url = movie_update.trailer_url
        updated_fields.append("trailer_url")
    if movie_update.category:
        valid_categories = ["Action", "Adventure", "Comedy", "Crime", "Documentary", "Drama", "Family",
                        "Fantasy", "Horror", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]
    categories = [cat.strip().capitalize() for cat in movie_update.category.split(",")]
    for category in categories:
        if category not in valid_categories:
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
    movie.category = ", ".join(categories)
    updated_fields.append("category")
    if movie_update.rating is not None: 
           movie.rating = movie_update.rating
           updated_fields.append("rating")
    if movie_update.actors is not None:
        actors = db.query(Actor).filter(Actor.id.in_(movie_update.actors)).all()
        if not actors:
            raise HTTPException(status_code=400, detail="No valid actors found")
        if len(actors) != len(movie_update.actors):
            raise HTTPException(status_code=400, detail="Some actors were not found")
        movie.actors = actors
        updated_fields.append("actors")

    if not updated_fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    db.commit()
    db.refresh(movie)
    return movie
@router.get("/add_movie")
def add_movie_page(
    request: Request, 
    db: Session = Depends(get_db)
):
    return templates.TemplateResponse("add_movie.html", {"request": request})

@router.get("/edit_movie/{movie_id}")
def edit_movie_page(
    request: Request, 
    movie_id: int, 
    db: Session = Depends(get_db) 
):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    all_actors = db.query(Actor).all()
    
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    return templates.TemplateResponse("edit_movie.html", {
        "request": request, 
        "movie": movie, 
        "all_actors": all_actors
    })

@router.delete("/movies/{movie_id}")
def delete_movie(
    movie_id: int, 
    db: Session = Depends(get_db), 
    current_admin: str = Depends(get_admin_user)  
):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Filma nav atrasta")

    db.delete(movie)
    db.commit()
    return {"message": "Filma veiksmīgi izdzēsta"}

@router.get("/delete_movie/{movie_id}")
def delete_movie_page(
    request: Request, 
    movie_id: int, 
    db: Session = Depends(get_db) 
):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Filma nav atrasta")
    return templates.TemplateResponse("delete_movie.html", {"request": request, "movie": movie})