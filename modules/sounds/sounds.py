import asyncio
import uuid
from datetime import datetime

from include import exceptions, models, schemas
from sqlalchemy import func
from sqlalchemy.orm import Session


class Sound():

    def get_record_count(self, db: Session):
        return db.query(models.Sound).count()

    def add_sound(self, request: schemas.SoundCreateRequest, db: Session):
        if not request or not hasattr(request, "data"):
            raise exceptions.BAD_REQUEST_EXCEPTION
        else:
            data = []
            if len(request.data) > 0:
                for item in request.data:
                    if not item.title:
                        raise exceptions.BAD_REQUEST_EXCEPTION
                    else:
                        newSound = models.Sound(
                            id=str(uuid.uuid4()),
                            title=item.title,
                            genres=item.genres,
                            bpm=item.bpm,
                            duration_in_seconds=item.duration_in_seconds)
                        db.add(newSound)
                        for credit in item.credits:
                            newCredit = models.Credit(
                                id=str(uuid.uuid4()),
                                name=credit.name,
                                role=credit.role,
                                sound_id=newSound.id)
                            db.add(newCredit)
                        data.append(
                            {"id": newSound.id, "title": newSound.title})
                db.commit()
            return {"data": data}

    def get_sound(self, soundId: str, db: Session):
        if not soundId:
            raise exceptions.BAD_REQUEST_EXCEPTION
        else:
            data = db.query(models.Sound).where(
                models.Sound.id == soundId).first()

            if not data:
                raise exceptions.NOT_FOUND_EXCEPTION
            else:
                return {"data": [data]}

    def get_list_of_sounds(self, limit: int, offset: int, db: Session):
        total_records = self.get_record_count(db)

        data = db.query(models.Sound).order_by(
            models.Sound.title.asc()).offset(offset).limit(limit).all()

        return {
            "data": data,
            "pagination": {
                "total_records": total_records,
                "count": len(data),
                "limit": limit,
                "offset": offset
            }
        }

    def get_recommendation(self, playlistId: str, db: Session):
        if not playlistId:
            raise exceptions.BAD_REQUEST_EXCEPTION
        else:
            playlist = db.query(models.Playlist.id).where(
                models.Playlist.id == playlistId).first()
            if not playlist:
                raise exceptions.NOT_FOUND_EXCEPTION
            else:
                data = []
                playlistSound = db.query(models.PlaylistSounds).where(
                    models.PlaylistSounds.playlist_id == playlistId).order_by(
                        models.PlaylistSounds.recommended.asc()).order_by(
                        models.PlaylistSounds.recommended_at.asc()).order_by(
                        func.random()).first()
                if playlistSound:
                    sound = db.query(models.Sound).where(
                        models.Sound.id == playlistSound.sound_id).first()
                    if sound:
                        details = {
                            "playlist_d": playlistId,
                            "sound_id": playlistSound.sound_id,
                            "updates": {
                                'recommended': playlistSound.recommended+1,
                                'recommended_at': datetime.now()}
                        }
                        data.append(sound)
                        self.update_recommended_sound(details, db)
                return {"data": data}

    def update_recommended_sound(self, details: dict, db: Session):
        db.query(models.PlaylistSounds).where(
            models.PlaylistSounds.playlist_id == details["playlist_d"]).where(
            models.PlaylistSounds.sound_id == details["sound_id"]).update(details["updates"])
        db.commit()
