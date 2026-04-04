from pydantic import BaseModel, Field

from backend.models.connection import Connection
from backend.models.item import Item
from backend.models.location import Location


class Map(BaseModel):
    locations: list[Location]
    connections: list[Connection] = Field(description="All connections that connect the locations to make the nodes and edges in the directed graph.")
    items: list[Item]