from datetime import datetime

from include.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship


class PlaylistSounds(Base):
    __tablename__ = "playlists_sounds"

    playlist_id = Column(ForeignKey('playlists.id'), primary_key=True)
    sound_id = Column(ForeignKey('sounds.id'), primary_key=True)
    position = Column(Integer, nullable=False)
    recommended = Column(Integer, default=0)
    recommended_at = Column(DateTime, default=datetime.now, nullable=False)

    playlists = relationship("Playlist", back_populates="sounds")
    sounds = relationship("Sound", back_populates="playlists")

    # proxies
    playlist_title = association_proxy(
        target_collection='playlists', attr='title')
    sound_title = association_proxy(target_collection='sounds', attr='title')


class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(String(36), primary_key=True, index=True)
    title = Column(String(255), nullable=False)

    sounds = relationship('PlaylistSounds', back_populates='playlists')
