import uuid

from include import models
from sqlalchemy.orm import Session
from test_data import testData


class Init():

    def add_test_data(db: Session):
        soundIds = ["",]
        for item in testData["sounds"]:
            newSound = models.Sound(
                id=str(uuid.uuid4()),
                title=item["title"],
                genres=item["genres"],
                bpm=item["bpm"],
                duration_in_seconds=item["duration_in_seconds"])
            db.add(newSound)
            soundIds.append(newSound.id)
            for credit in item["credits"]:
                newCredit = models.Credit(
                    id=str(uuid.uuid4()),
                    name=credit["name"],
                    role=credit["role"],
                    sound_id=newSound.id)
                db.add(newCredit)
        for item in testData["playlists"]:
            newPlaylist = models.Playlist(
                id=str(uuid.uuid4()),
                title=item["title"])
            db.add(newPlaylist)
            soundPosition = 1
            for soundIndex in item["sounds"]:
                newPlaylistsSounds = models.PlaylistSounds(
                    playlist_id=newPlaylist.id,
                    sound_id=soundIds[soundIndex],
                    position=soundPosition)
                db.add(newPlaylistsSounds)
                soundPosition += 1
        db.commit()
        return {
            "data": {
                "sounds_added": len(testData['sounds']),
                "playlists_added": len(testData['playlists'])
            }
        }

    def delete_all_data(db: Session):
        records = db.query(models.Credit).where(True)
        if records:
            records.delete()
        records = db.query(models.Playlist).where(True)
        if records:
            records.delete()
        records = db.query(models.PlaylistSounds).where(True)
        if records:
            records.delete()
        records = db.query(models.Sound).where(True)
        if records:
            records.delete()
        db.commit()
