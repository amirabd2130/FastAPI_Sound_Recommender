from fastapi import APIRouter, Depends, status
from include import database, schemas
from modules.playlists.playlists import Playlist
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/playlists",
    tags=["Playlists"],
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PlaylistCreateResponse)
def add_playlist(request: schemas.PlaylistCreateRequest, db: Session = Depends(database.get_db)):
    return Playlist.add_playlist(request, db)
