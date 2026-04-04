from pydantic import BaseModel, Field

from backend.models.direction import Direction


class Connection(BaseModel):
    source_location: str
    target_location: str
    # direction: Direction = Field(description="the cardinal direction that it takes to go from the source to target location. Valid directions: north, south, east, west, northeast, northwest, southeast, southwest, up, down, in, out")
    direction: str = Field(description="the cardinal direction that it takes to go from the source to target location. Valid directions: north, south, east, west, northeast, northwest, southeast, southwest, up, down, in, out")
