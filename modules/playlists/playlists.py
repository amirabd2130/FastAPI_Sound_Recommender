import uuid

from include import exceptions, models, schemas
from sqlalchemy.orm import Session


class Playlist():
    def add_playlist(request: schemas.PlaylistCreateRequest, db: Session):
        if not request or not hasattr(request, "data"):
            raise exceptions.BAD_REQUEST_EXCEPTION
        else:
            data = []
            if len(request.data) > 0:
                for item in request.data:
                    newPlaylist = models.Playlist(
                        id=str(uuid.uuid4()),
                        title=item.title)
                    db.add(newPlaylist)
                    soundPosition = 1
                    for sound in item.sounds:
                        newPlaylistsSounds = models.PlaylistSounds(
                            playlist_id=newPlaylist.id,
                            sound_id=sound,
                            position=soundPosition)
                        db.add(newPlaylistsSounds)
                        soundPosition += 1
                    data.append(
                        {"id": newPlaylist.id, "title": newPlaylist.title})
                db.commit()
            return {"data": data}

    def get_playlist(id: str, db: Session):
        if not id:
            raise exceptions.BAD_REQUEST_EXCEPTION
        else:
            playlist = db.query(models.Playlist).where(
                models.Playlist.id == id).first()

            if not playlist:
                raise exceptions.NOT_FOUND_EXCEPTION
            else:
                return playlist
