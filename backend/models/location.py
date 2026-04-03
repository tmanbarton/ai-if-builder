from pydantic import BaseModel

from backend.models.connection import Connection
from backend.models.item import Item
from backend.models.scenery_opject import SceneryObject


class Location(BaseModel):
    key: str
    short_description: str
    long_description: str
    visited: bool | None = False
    is_starting_location: bool | None = False
    is_openable: bool | None = False
    is_container: bool | None = False
    connections: list[Connection]
    scenery_objects: list[SceneryObject]