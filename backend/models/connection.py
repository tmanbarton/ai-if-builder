from pydantic import BaseModel, Field

from backend.models.direction import Direction


class Connection(BaseModel):
    source_location: str = Field(description="the key of the location this connection starts from for the directed graph structure")
    target_location: str = Field(description="the key of the location this connection goes to for the directed graph structure")
    direction: Direction = Field(description="the cardinal direction that it takes to go from the source to target location. Valid directions: north, south, east, west, northeast, northwest, southeast, southwest, up, down, in, out")