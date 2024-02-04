import os

from include import exceptions
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


FASTAPI_SOUND_RECOMMENDER_DATABASE_URL = os.environ.get(
    "FASTAPI_SOUND_RECOMMENDER_DATABASE_URL")
if not FASTAPI_SOUND_RECOMMENDER_DATABASE_URL:
    raise exceptions.DATABASE_ERROR
else:
    engine = create_engine(FASTAPI_SOUND_RECOMMENDER_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
