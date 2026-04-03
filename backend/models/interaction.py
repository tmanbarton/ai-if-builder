from pydantic import BaseModel

from backend.models.interaction_type import InteractionType


class Interaction(BaseModel):
    interaction_type: InteractionType
    description: str