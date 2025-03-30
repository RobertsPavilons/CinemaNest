from fastapi import APIRouter, Depends, HTTPException, Form 
from sqlalchemy.orm import Session
from database import get_db
from models import TVShow, Actor, tvshow_actors
from routers.schemas import TVShowCreate, TVShowResponse, TVShowUpdate, ActorCreate, ActorResponse
from routers.auth import get_admin_user
from typing import List
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/tvshows", response_model=list[TVShowResponse])
def get_tvshows(db: Session = Depends(get_db)):
    return db.query(TVShow).all()

@router.get("/tvshowlist")
def tvshow_page(request: Request):
    return templates.TemplateResponse("tvshows.html", {"request": request})

@router.get("/tvshows/{tvshow_id}", response_model=TVShowResponse)
def get_tvshow(tvshow_id: int, db: Session = Depends(get_db)):
    tvshow = db.query(TVShow).filter(TVShow.id == tvshow_id).first()
    if not tvshow:
        raise HTTPException(status_code=404, detail="TV show not found")
    return tvshow

@router.get("/tvshowlist/{id}")
def tvshow_details(id: int, request: Request, db: Session = Depends(get_db)):
    tvshow = db.query(TVShow).filter(TVShow.id == id).first()
    if not tvshow:
        raise HTTPException(status_code=404, detail="Filma nav atrasta")

    return templates.TemplateResponse("tvshow.html", {
        "request": request,
        "tvshow": tvshow
    })

@router.post("/tvshows", response_model=TVShowResponse)
def add_tvshow(
    tvshow: TVShowCreate, 
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_admin_user)
):
    new_tvshow = TVShow(
        title=tvshow.title,
        description=tvshow.description,
        year=tvshow.year,
        seasons=tvshow.seasons,
        poster_url=tvshow.poster_url,
        trailer_url=tvshow.trailer_url,
        category=tvshow.category,
        rating=tvshow.rating
    )

    if tvshow.actors:
        actors = db.query(Actor).filter(Actor.id.in_(tvshow.actors)).all()
        new_tvshow.actors = actors

    db.add(new_tvshow)
    db.commit()
    db.refresh(new_tvshow)
    return new_tvshow

@router.put("/tvshows/{tvshow_id}", response_model=TVShowResponse)
def update_tvshow(
    tvshow_id: int, 
    tvshow_update: TVShowUpdate, 
    db: Session = Depends(get_db), 
    current_admin: str = Depends(get_admin_user)  
):
    tvshow = db.query(TVShow).filter(TVShow.id == tvshow_id).first()
    if not tvshow:
        raise HTTPException(status_code=404, detail="TV Show not found")

    updated_fields = []
    if tvshow_update.title:
        tvshow.title = tvshow_update.title
        updated_fields.append("title")
    if tvshow_update.description:
        tvshow.description = tvshow_update.description
        updated_fields.append("description")
    if tvshow_update.year:
        tvshow.year = tvshow_update.year
        updated_fields.append("year")
    if tvshow_update.seasons:
        tvshow.seasons = tvshow_update.seasons
        updated_fields.append("seasons")
    if tvshow_update.poster_url:
        tvshow.poster_url = tvshow_update.poster_url
        updated_fields.append("poster_url")
    if tvshow_update.trailer_url:
        tvshow.trailer_url = tvshow_update.trailer_url
        updated_fields.append("trailer_url")
    if tvshow_update.category:
        valid_categories = ["Action", "Adventure", "Comedy", "Crime", "Documentary", "Drama", "Family",
                        "Fantasy", "Horror", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]
    
    categories = [cat.strip().capitalize() for cat in tvshow_update.category.split(",")]
    
    for category in categories:
        if category not in valid_categories:
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
    
    tvshow.category = ", ".join(categories)
    updated_fields.append("category")
    if tvshow_update.rating is not None:
           tvshow.rating = tvshow_update.rating
           updated_fields.append("rating")
    if tvshow_update.actors is not None:
        actors = db.query(Actor).filter(Actor.id.in_(tvshow_update.actors)).all()
        if not actors:
            raise HTTPException(status_code=400, detail="No valid actors found")
        if len(actors) != len(tvshow_update.actors):
            raise HTTPException(status_code=400, detail="Some actors were not found")
        tvshow.actors = actors
        updated_fields.append("actors")

    if not updated_fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    db.commit()
    db.refresh(tvshow)
    return tvshow
@router.get("/add_tvshow")
def add_tvshow_page(
    request: Request, 
    db: Session = Depends(get_db)
):
    return templates.TemplateResponse("add_tvshow.html", {"request": request})

@router.get("/edit_tvshow/{tvshow_id}")
def edit_tvshow_page(
    request: Request, 
    tvshow_id: int, 
    db: Session = Depends(get_db) 
):
    tvshow = db.query(TVShow).filter(TVShow.id == tvshow_id).first()
    all_actors = db.query(Actor).all()
    
    if not tvshow:
        raise HTTPException(status_code=404, detail="Movie not found")

    return templates.TemplateResponse("edit_TVShow.html", {
        "request": request, 
        "movie": tvshow, 
        "all_actors": all_actors
    })

@router.delete("/tvshows/{tvshow_id}")
def delete_tvshow(
    tvshow_id: int, 
    db: Session = Depends(get_db), 
    current_admin: str = Depends(get_admin_user)  
):
    tvshow = db.query(TVShow).filter(TVShow.id == tvshow_id).first()
    if not tvshow:
        raise HTTPException(status_code=404, detail="Filma nav atrasta")

    db.delete(tvshow)
    db.commit()
    return {"message": "Filma veiksmīgi izdzēsta"}

@router.get("/delete_tvshow/{tvshow_id}")
def delete_tvshow_page(
    request: Request, 
    tvshow_id: int, 
    db: Session = Depends(get_db) 
):
    tvshow = db.query(TVShow).filter(TVShow.id == tvshow_id).first()
    if not tvshow:
        raise HTTPException(status_code=404, detail="Filma nav atrasta")
    return templates.TemplateResponse("delete_tvshow.html", {"request": request, "tvshow": tvshow})

