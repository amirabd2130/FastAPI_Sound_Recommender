from fastapi import APIRouter, Depends, status
from include import database, schemas
from modules.init.init import Init
from modules.sounds.sounds import Sound
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get("/init", status_code=status.HTTP_201_CREATED, response_model=dict)
def add_test_data(db: Session = Depends(database.get_db)):

    return Init().add_test_data(db)


@router.delete("/cleanup", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_data(db: Session = Depends(database.get_db)):
    return Init().delete_all_data(db)


@router.post("/sounds", status_code=status.HTTP_201_CREATED, response_model=schemas.SoundCreateResponse)
def add_sound(request: schemas.SoundCreateRequest, db: Session = Depends(database.get_db)):
    return Sound().add_sound(request, db)
