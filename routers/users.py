from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from routers.auth import get_current_user
from .schemas import UserResponse, UserUpdate
from .auth import pwd_context, templates

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()  
    return {"users": [{"id": i.id, "username": i.username, "role": i.role} for i in users]}

@router.get("/edit_accountdata")
def login(request: Request):
    return templates.TemplateResponse("edit_accountdata.html", {"request": request})

@router.put("/update_account", response_model=UserResponse)
def update_account(
    user_update: UserUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Lietotājs nav atrasts")

    if not any([user_update.username, user_update.password]):
        raise HTTPException(status_code=400, detail="No fields to update")

    if user_update.username:
        existing_user = db.query(User).filter(User.username == user_update.username).first()
        if existing_user and existing_user.id != user.id:
            raise HTTPException(status_code=400, detail="Username already taken by another user.")
        user.username = user_update.username

    if user_update.password:
        user.password = pwd_context.hash(user_update.password)

    db.commit()
    db.refresh(user)
    
    return user

