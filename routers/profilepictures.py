from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import ProfilePicture, User
from routers.schemas import ProfilePictureCreate, ProfilePictureResponse
from routers.auth import get_current_user
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from routers.auth import get_admin_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/add_profilepictures")
def add_profile_picture_page(request: Request):
    return templates.TemplateResponse("add_profilepicture.html", {"request": request})

@router.get("/profilepictures", response_model=list[ProfilePictureResponse])
def get_profile_pictures(db: Session = Depends(get_db)):
    return db.query(ProfilePicture).all()


@router.post("/profilepictures", response_model=ProfilePictureResponse)
def add_profile_picture(profile_data: ProfilePictureCreate, db: Session = Depends(get_db), current_admin: str = Depends(get_admin_user)):
    existing_picture = db.query(ProfilePicture).filter(ProfilePicture.name == profile_data.name).first()
    if existing_picture:
        raise HTTPException(status_code=400, detail="Profile picture already exists.")

    new_picture = ProfilePicture(name=profile_data.name, image_url=profile_data.image_url)
    db.add(new_picture)
    db.commit()
    db.refresh(new_picture)

    return new_picture

@router.get("/delete_profilepicture/{profile_picture_id}")
async def delete_profile_picture(profile_picture_id: int, request: Request, db: Session = Depends(get_db)):
    profile_picture = db.query(ProfilePicture).filter(ProfilePicture.id == profile_picture_id).first()
    if not profile_picture:
        raise HTTPException(status_code=404, detail="Profile picture not found")
    
    return templates.TemplateResponse("delete_profilepicture.html", {"request": request, "profile_picture": profile_picture})

@router.delete("/profilepictures/{picture_id}")
async def delete_profile_picture(picture_id: int, db: Session = Depends(get_db), current_admin: str = Depends(get_admin_user)):
    profile_picture = db.query(ProfilePicture).filter(ProfilePicture.id == picture_id).first()

    if not profile_picture:
        raise HTTPException(status_code=404, detail="Profile picture not found")

    db.delete(profile_picture)
    db.commit()
    return {"message": "Profile picture deleted successfully"}

@router.get("/change_profilepicture")
def add_profile_picture_page(request: Request):
    return templates.TemplateResponse("edit_profilepicture.html", {"request": request})

@router.put("/profilepictures/{picture_id}")
async def change_profile_picture(
    picture_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Lietotājs nav atrasts")

    picture = db.query(ProfilePicture).filter(ProfilePicture.id == picture_id).first()
    if not picture:
        raise HTTPException(status_code=404, detail="Profila bilde nav atrasta")
    user.profile_picture_id = picture.id  

    db.commit()
    db.refresh(user)

    return {"message": "Profila bilde veiksmīgi nomainīta", "new_picture_id": picture.id}


