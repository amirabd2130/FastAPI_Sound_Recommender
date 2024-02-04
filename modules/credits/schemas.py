from pydantic import BaseModel


class Credit(BaseModel):
    name: str
    role: str
