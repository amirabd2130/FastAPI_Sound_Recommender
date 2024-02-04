from include.database import Base
from sqlalchemy import JSON, Column, Integer, String
from sqlalchemy.orm import relationship


class Sound(Base):
    __tablename__ = "sounds"

    id = Column(String(36), primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    genres = Column(JSON, nullable=True)
    bpm = Column(Integer, nullable=True)
    duration_in_seconds = Column(Integer, nullable=True)

    credits = relationship('Credit', back_populates='sounds')

    playlists = relationship('PlaylistSounds', back_populates='sounds')
