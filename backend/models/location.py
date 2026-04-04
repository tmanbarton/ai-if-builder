from pydantic import BaseModel, Field

from backend.models.connection import Connection
from backend.models.item import Item
from backend.models.scenery_opject import SceneryObject


class Location(BaseModel):
    name: str = Field(description="The unique name of the location, used as a key.")
    short_description: str
    long_description: str
    visited: bool | None = False
    is_starting_location: bool | None = False
    is_openable: bool | None = Field(default=False, description="Whether or not the location itself is openable. Example: location is a shed, which can be opened. Negative example: Location has a lockbox at it, but the locatio isn't a lockbox, so the location istelf isn't openable.")
    scenery_objects: list[SceneryObject] = []