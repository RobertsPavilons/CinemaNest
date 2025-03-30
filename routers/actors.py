from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
from models import Actor
from routers.schemas import ActorCreate, ActorResponse
from routers.auth import get_admin_user
from typing import List
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/actors", response_model=List[ActorResponse])
def get_actors(db: Session = Depends(get_db)):
    actors = db.query(Actor).order_by(Actor.name).all()
    return actors

@router.get("/add_actor")
def add_actor_page(
    request: Request, 
    db: Session = Depends(get_db)
):
    return templates.TemplateResponse("add_actor.html", {"request": request})

@router.get("/actorslist")
def add_actor_page(
    request: Request, 
    db: Session = Depends(get_db)
):
    return templates.TemplateResponse("actors.html", {"request": request})

@router.post("/actors")
def add_actor(
    actor: ActorCreate, 
    db: Session = Depends(get_db), 
    current_admin: str = Depends(get_admin_user)  
):
    existing_actor = db.query(Actor).filter(Actor.name == actor.name).first()
    if existing_actor:
        raise HTTPException(status_code=400, detail="Actor already exists")

    new_actor = Actor(name=actor.name, image_url=actor.image_url)
    db.add(new_actor)
    db.commit()
    db.refresh(new_actor)

    return new_actor