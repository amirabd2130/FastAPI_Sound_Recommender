from typing import Annotated, Union

from annotated_types import Ge
from fastapi import APIRouter, Depends, status
from include import database, schemas
from modules.sounds.sounds import Sound
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/sounds",
    tags=["Sounds"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=schemas.SoundListPaginated)
def get_list_of_sounds(limit: Annotated[int, Ge(0)] = 10, offset: Annotated[int, Ge(0)] = 0, db: Session = Depends(database.get_db)):
    return Sound.get_list_of_sounds(limit, offset, db)


@router.get("/get", status_code=status.HTTP_200_OK, response_model=schemas.SoundFullResponse)
def get_sound(soundId: str, db: Session = Depends(database.get_db)):
    return Sound.get_sound(soundId, db)


@router.get("/recommended", status_code=status.HTTP_200_OK, response_model=Union[schemas.SoundFullResponse, dict])
def get_recommendation(playlistId: str, db: Session = Depends(database.get_db)):
    return Sound.get_recommendation(playlistId, db)
