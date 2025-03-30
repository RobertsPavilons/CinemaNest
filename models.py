from sqlalchemy import Table, Column, Integer, String, ForeignKey, Text, Float, Enum
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, JSON
from sqlalchemy.orm import relationship
from database import Base
from datetime import date
import enum


class ProfilePicture(Base):
    __tablename__ = "profile_pictures"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    image_url = Column(String, nullable=False)
    users = relationship("User", back_populates="profile_picture")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="user")
    profile_picture_id = Column(Integer, ForeignKey("profile_pictures.id"), nullable=True)  
    profile_picture = relationship("ProfilePicture", back_populates="users")   

movie_actors = Table(
    "movie_actors",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id")),
    Column("actor_id", Integer, ForeignKey("actors.id"))
)
tvshow_actors = Table(
    "tvshow_actors",
    Base.metadata,
    Column("tvshow_id", Integer, ForeignKey("tvshows.id")),
    Column("actor_id", Integer, ForeignKey("actors.id"))
)

animationmovie_actors = Table(
    "animationmovie_actors",
    Base.metadata,
    Column("animationmovie_id", Integer, ForeignKey("animationmovies.id")),
    Column("actor_id", Integer, ForeignKey("actors.id"))
)


class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    image_url = Column(String, nullable=True)
    movies = relationship("Movie", secondary=movie_actors, back_populates="actors")
    tvshows = relationship("TVShow", secondary=tvshow_actors, back_populates="actors")
    animationmovies = relationship("AnimationMovie", secondary=animationmovie_actors, back_populates="actors")


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    year = Column(Integer)
    poster_url = Column(String, nullable=True)
    trailer_url = Column(String, nullable=True)
    category = Column(String, nullable=True)
    rating = Column(Float)
    actors = relationship("Actor", secondary=movie_actors, back_populates="movies")

class TVShow(Base):
    __tablename__ = "tvshows"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    year = Column(Integer)
    seasons = Column(Integer)
    poster_url = Column(String, nullable=True)
    trailer_url = Column(String, nullable=True)
    category = Column(String, nullable=True)
    rating = Column(Float)
    actors = relationship("Actor", secondary=tvshow_actors, back_populates="tvshows")

class AnimationMovie(Base):
    __tablename__ = "animationmovies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    year = Column(Integer)
    poster_url = Column(String, nullable=True)
    trailer_url = Column(String, nullable=True)
    category = Column(String, nullable=True)
    rating = Column(Float)
    actors = relationship("Actor", secondary=animationmovie_actors, back_populates="animationmovies") 