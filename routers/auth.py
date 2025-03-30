from dotenv import load_dotenv
from pydantic import BaseModel
import os
import sys
from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal 
from models import User, ProfilePicture
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .schemas import UserCreate, UserResponse
import bcrypt
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordRequestForm

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter()
templates = Jinja2Templates(directory="templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

def get_admin_user(current_user: User = Depends(get_current_user)):
    sys.stdout.flush()
    if not isinstance(current_user, User):
        print("❌ ERROR: current_user NAV User objekts!")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    return current_user

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

admin_data = {"sub": "admin_user", "role": "admin"}
access_token = create_access_token(admin_data, timedelta(minutes=30))


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(days=7))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)

@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register")
def register(request: Request, db: Session = Depends(get_db)):
    profile_pictures = db.query(ProfilePicture).all()
    return templates.TemplateResponse("register.html", {"request": request, "profile_pictures": profile_pictures})

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered!")

    hashed_password = pwd_context.hash(user.password)
    profile_picture_entry = db.query(ProfilePicture).filter(ProfilePicture.id == user.profile_picture).first()
    if not profile_picture_entry:
        raise HTTPException(status_code=400, detail="Invalid profile picture selection.")

    db_user = User(
        username=user.username,
        password=hashed_password,
        profile_picture_id=profile_picture_entry.id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user



class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == login_data.username).first()
    if not user or not pwd_context.verify(login_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_refresh_token(data={"sub": user.username}, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

    return {
        "access_token": access_token, 
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
async def refresh_token(refresh_token: str = Form(...)):
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        new_access_token = create_access_token(data={"sub": username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return {"access_token": new_access_token, "token_type": "bearer"}
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
@router.post("/token")
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    
    return {"access_token": access_token, "token_type": "bearer"}
@router.get("/me")
def get_current_user_route(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        profile_picture = db.query(ProfilePicture).filter(ProfilePicture.id == user.profile_picture_id).first()
        image_url = profile_picture.image_url if profile_picture else "/static/default-profile.jpg"

        return {
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "profile_picture": image_url
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    
