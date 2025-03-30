from fastapi import APIRouter, Depends, HTTPException, Form 
from sqlalchemy.orm import Session
from database import get_db
from models import AnimationMovie, Actor, animationmovie_actors
from routers.schemas import AnimationMovieCreate, AnimationMovieResponse, AnimationMovieUpdate, ActorCreate, ActorResponse
from routers.auth import get_admin_user
from typing import List
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/animationmovies", response_model=list[AnimationMovieResponse])
def get_animationmovies(db: Session = Depends(get_db)):
    return db.query(AnimationMovie).all()

@router.get("/animationmovielist")
def animationmovie_page(request: Request):
    return templates.TemplateResponse("animationmovies.html", {"request": request})

@router.get("/animationmovies/{animationmovie_id}", response_model=AnimationMovieResponse)
def get_animationmovie(animationmovie_id: int, db: Session = Depends(get_db)):
    animationmovie = db.query(AnimationMovie).filter(AnimationMovie.id == animationmovie_id).first()
    if not animationmovie:
        raise HTTPException(status_code=404, detail="Animation movie not found")
    return animationmovie

@router.get("/animationmovielist/{id}")
def animationmovie_details(id: int, request: Request, db: Session = Depends(get_db)):
    animationmovie = db.query(AnimationMovie).filter(AnimationMovie.id == id).first()
    if not animationmovie:
        raise HTTPException(status_code=404, detail="Animation movie not found")

    return templates.TemplateResponse("animationmovie.html", {
        "request": request,
        "animationmovie": animationmovie
    })

@router.post("/animationmovies", response_model=AnimationMovieResponse)
def add_animationmovie(
    animationmovie: AnimationMovieCreate, 
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_admin_user)
):
    new_animationmovie = AnimationMovie(
        title=animationmovie.title,
        description=animationmovie.description,
        year=animationmovie.year,
        poster_url=animationmovie.poster_url,
        trailer_url=animationmovie.trailer_url,
        category=animationmovie.category,
        rating=animationmovie.rating
    )

    if animationmovie.actors:
        actors = db.query(Actor).filter(Actor.id.in_(animationmovie.actors)).all()
        new_animationmovie.actors = actors

    db.add(new_animationmovie)
    db.commit()
    db.refresh(new_animationmovie)
    return new_animationmovie

@router.put("/animationmovies/{animationmovie_id}", response_model=AnimationMovieResponse)
def update_animationmovie(
    animationmovie_id: int, 
    animationmovie_update: AnimationMovieUpdate, 
    db: Session = Depends(get_db), 
    current_admin: str = Depends(get_admin_user)  
):
    animationmovie = db.query(AnimationMovie).filter(AnimationMovie.id == animationmovie_id).first()
    if not animationmovie:
        raise HTTPException(status_code=404, detail="Animation movie not found")

    updated_fields = []
    if animationmovie_update.title:
        animationmovie.title = animationmovie_update.title
        updated_fields.append("title")
    if animationmovie_update.description:
        animationmovie.description = animationmovie_update.description
        updated_fields.append("description")
    if animationmovie_update.year:
        animationmovie.year = animationmovie_update.year
        updated_fields.append("year")
    if animationmovie_update.poster_url:
        animationmovie.poster_url = animationmovie_update.poster_url
        updated_fields.append("poster_url")
    if animationmovie_update.trailer_url:
        animationmovie.trailer_url = animationmovie_update.trailer_url
        updated_fields.append("trailer_url")
    if animationmovie_update.category:
        valid_categories = ["Animation"]
        if animationmovie_update.category not in valid_categories:
            raise HTTPException(status_code=400, detail="Invalid category")
        animationmovie.category = animationmovie_update.category
        updated_fields.append("category")
    if animationmovie_update.rating is not None:
        animationmovie.rating = animationmovie_update.rating
        updated_fields.append("rating")
    if animationmovie_update.actors is not None:
        actors = db.query(Actor).filter(Actor.id.in_(animationmovie_update.actors)).all()
        if not actors:
            raise HTTPException(status_code=400, detail="No valid actors found")
        if len(actors) != len(animationmovie_update.actors):
            raise HTTPException(status_code=400, detail="Some actors were not found")
        animationmovie.actors = actors
        updated_fields.append("actors")

    if not updated_fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    db.commit()
    db.refresh(animationmovie)
    return animationmovie

@router.get("/add_animationmovie")
def add_animationmovie_page(
    request: Request, 
    db: Session = Depends(get_db)
):
    return templates.TemplateResponse("add_animationmovie.html", {"request": request})

@router.get("/edit_animationmovie/{animationmovie_id}")
def edit_animationmovie_page(
    request: Request, 
    animationmovie_id: int, 
    db: Session = Depends(get_db) 
):
    animationmovie = db.query(AnimationMovie).filter(AnimationMovie.id == animationmovie_id).first()
    all_actors = db.query(Actor).all()
    
    if not animationmovie:
        raise HTTPException(status_code=404, detail="Animation movie not found")

    return templates.TemplateResponse("edit_animationmovie.html", {
        "request": request, 
        "animationmovie": animationmovie, 
        "all_actors": all_actors
    })

@router.delete("/animationmovies/{animationmovie_id}")
def delete_animationmovie(
    animationmovie_id: int, 
    db: Session = Depends(get_db), 
    current_admin: str = Depends(get_admin_user)  
):
    animationmovie = db.query(AnimationMovie).filter(AnimationMovie.id == animationmovie_id).first()
    if not animationmovie:
        raise HTTPException(status_code=404, detail="Animation movie not found")

    db.delete(animationmovie)
    db.commit()
    return {"message": "Animation movie successfully deleted"}

@router.get("/delete_animationmovie/{animationmovie_id}")
def delete_animationmovie_page(
    request: Request, 
    animationmovie_id: int, 
    db: Session = Depends(get_db) 
):
    animationmovie = db.query(AnimationMovie).filter(AnimationMovie.id == animationmovie_id).first()
    if not animationmovie:
        raise HTTPException(status_code=404, detail="Animation movie not found")
    return templates.TemplateResponse("delete_animationmovie.html", {"request": request, "animationmovie": animationmovie})


