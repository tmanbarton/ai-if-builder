from pydantic import BaseModel

from backend.models.direction import Direction


class Connection(BaseModel):
    source_location: str
    target_location: str
    direction: Direction