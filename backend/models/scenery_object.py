from pydantic import BaseModel, Field

from backend.models.interaction import Interaction

class SceneryObject(BaseModel):
    name: str = Field(description="The unique name of the scenery object, used as a key for identifying it and for checking the user's input. Starts with a lowercase letter and words separated by spaces.")
    is_container: bool | None = Field(default=False, description="Whether or not this scenery object should be able to hold items and be treated as a container.")
    interactions: list[Interaction] = []

