from pydantic import BaseModel, Field

from backend.models.connection import Connection
from backend.models.item import Item
from backend.models.scenery_opject import SceneryObject


class Location(BaseModel):
    key: str = Field(description="The unique name of the location, used as a key.")
    short_description: str = Field(description="The short description of the location for when the user has already visited the location.")
    long_description: str = Field(description="The long description of the location for when the user first visits the location or uses the 'look' command.")
    visited: bool | None = Field(default=False, description="Whether or not the location has been visited.")
    is_starting_location: bool | None = Field(default=False, description="Whether or not this is the starting location of the game.")
    is_openable: bool | None = Field(default=False, description="Whether or not the location itself is openable. Example: location is a shed, which can be opened. Negative example: Location has a lockbox at it, but the locatio isn't a lockbox, so the location istelf isn't openable.")
    scenery_objects: list[SceneryObject] = Field(default=[], description="List of all scenery objects. Empty if none are provided.")