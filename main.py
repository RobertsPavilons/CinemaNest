from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from database import engine, Base
from routers import auth, movies, users, actors, tvshows, animationmovies, random, profilepictures
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from database import SessionLocal
from models import User
from passlib.context import CryptContext
from routers.auth import router as auth_router
from routers.movies import router as actors_router
from routers.auth import get_admin_user, get_current_user
from fastapi.responses import HTMLResponse

app = FastAPI(docs_url=None, redoc_url=None)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Izveido datubāzi
Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

# Pievienojam maršrutus
app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(users.router)
app.include_router(actors.router)
app.include_router(tvshows.router)
app.include_router(animationmovies.router)
app.include_router(random.router)
app.include_router(profilepictures.router)


@app.get("/", response_class=HTMLResponse)
async def serve_homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/home")
def serve_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/login")
def serve_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register")
def serve_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
