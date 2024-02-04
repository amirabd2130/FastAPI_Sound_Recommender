from typing import List

from include.schemas import ListPagination
from pydantic import BaseModel
from modules.credits import schemas as credits_schema


class Sound(BaseModel):
    id: str
    title: str
    genres: list
    bpm: int
    duration_in_seconds: int
    credits: List[credits_schema.Credit]


class SoundFull(BaseModel):
    title: str
    genres: list
    bpm: int
    duration_in_seconds: int
    credits: List[credits_schema.Credit]


class SoundMinimal(BaseModel):
    id: str
    title: str


class SoundCreate(BaseModel):
    title: str
    genres: list
    bpm: int
    duration_in_seconds: int
    credits: List[credits_schema.Credit]


class SoundCreateRequest(BaseModel):
    data: List[SoundCreate]


class SoundCreateResponse(BaseModel):
    data: List[SoundMinimal]


class SoundFullResponse(BaseModel):
    data: List[SoundFull]


class SoundListPaginated(BaseModel):
    data: List[Sound] = []
    pagination: ListPagination
