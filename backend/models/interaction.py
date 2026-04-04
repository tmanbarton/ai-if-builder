from pydantic import BaseModel, Field

from backend.models.interaction_type import InteractionType


class Interaction(BaseModel):
    # interaction_type: InteractionType = Field(description="The type of this interaction. Valid types: 'climb', 'drink', 'eat', 'kick', 'look', 'bunch', 'read', 'swim', 'take'")
    interaction_type: str = Field(description="The type of this interaction. Valid types: 'climb', 'drink', 'eat', 'kick', 'look', 'bunch', 'read', 'swim', 'take'")
    response_description: str = Field(description="A string that is the exact response to provide when the user does the interaction. Example: 'You stub your toe and it really hurts now. Best not to try that again.'")
