import uuid

from include import exceptions, models, schemas
from sqlalchemy.orm import Session


class Playlist():
    def add_playlist(self, request: schemas.PlaylistCreateRequest, db: Session):
        if not request or not hasattr(request, "data"):
            raise exceptions.BAD_REQUEST_EXCEPTION
        else:
            data = []
            if len(request.data) > 0:
                for item in request.data:
                    if not item.title:
                        raise exceptions.BAD_REQUEST_EXCEPTION
                    else:
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
