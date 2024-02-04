from include.database import Base
from modules.sounds.models import *
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship


class Credit(Base):
    __tablename__ = 'credits'

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(100))
    role = Column(String(50))

    sound_id = Column(String(36), ForeignKey("sounds.id"))
    sounds = relationship("Sound", back_populates="credits")
