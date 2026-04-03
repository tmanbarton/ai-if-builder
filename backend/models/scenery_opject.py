from pydantic import BaseModel, Field

from backend.models.interaction import Interaction

class SceneryObject(BaseModel):
    key: str = Field(description="The unique name of the scenery object, used as a key for identifying it.")
    is_container: bool | None = Field(default=False, description="Whether or not this scenery object should be able to hold items and be treated as a container.")
    interactions: list[Interaction] = Field(default=[], description="A list of possible interactions for this scenery object.")
