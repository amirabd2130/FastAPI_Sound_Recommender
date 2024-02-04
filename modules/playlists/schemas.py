from typing import List

from modules.sounds import schemas as sounds_schema
from pydantic import BaseModel


class Playlist(BaseModel):
    id: str
    title: str
    sounds: List[sounds_schema.Sound]


class PlaylistMinimal(BaseModel):
    id: str
    title: str


class PlaylistCreate(BaseModel):
    title: str
    sounds: List[str]


class PlaylistCreateRequest(BaseModel):
    data: List[PlaylistCreate]


class PlaylistCreateResponse(BaseModel):
    data: List[PlaylistMinimal]
