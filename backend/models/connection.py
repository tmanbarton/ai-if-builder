from pydantic import BaseModel, Field

class Connection(BaseModel):
    source_location: str
    target_location: str
    direction: str = Field(description="The cardinal direction that it takes to go from the source to target location. Valid directions: 'NORTH', 'SOUTH', 'EAST', 'WEST', 'NORTHEAST', 'NORTHWEST', 'SOUTHWEST', 'SOUTHEAST', 'UP', 'DOWN', 'IN', 'OUT'. MUST BE IN ALL CAPS!!")
