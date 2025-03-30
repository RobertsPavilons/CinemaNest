from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from enum import Enum
import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    profile_picture: Optional[str] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

class ProfilePictureCreate(BaseModel):
    name: str
    image_url: str

class ProfilePictureResponse(ProfilePictureCreate):
    id: int

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    class Config:
        from_attributes = True

class ActorCreate(BaseModel):
    name: str
    image_url: Optional[str] = None

class ActorResponse(ActorCreate):
    id: int

class MovieCreate(BaseModel):
    title: str
    description: str
    year: int
    poster_url: Optional[str] = None
    trailer_url: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[float] = None
    actors: Optional[List[int]] = None

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    year: Optional[int] = None
    poster_url: Optional[str] = None
    trailer_url: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[float] = None
    actors: Optional[List[int]] = None

class MovieResponse(MovieCreate):
    id: int
    actors: Optional[List[ActorResponse]] = None


class TVShowCreate(BaseModel):
    title: str
    description: str
    year: int
    seasons: int  
    poster_url: Optional[str] = None
    trailer_url: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[float] = None
    actors: Optional[List[int]] = None

class TVShowUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    year: Optional[int] = None
    seasons: Optional[int] = None
    poster_url: Optional[str] = None
    trailer_url: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[float] = None
    actors: Optional[List[int]] = None

class TVShowResponse(TVShowCreate):
    id: int
    actors: Optional[List[ActorResponse]] = None

class AnimationMovieCreate(BaseModel):
    title: str
    description: str
    year: int
    poster_url: Optional[str] = None
    trailer_url: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[float] = None
    actors: Optional[List[int]] = None

class AnimationMovieUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    year: Optional[int] = None
    poster_url: Optional[str] = None
    trailer_url: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[float] = None
    actors: Optional[List[int]] = None

class AnimationMovieResponse(AnimationMovieCreate):
    id: int
    actors: Optional[List[ActorResponse]] = None
