from pydantic import BaseModel, Field


class Hint(BaseModel):
    condition: str = Field(description="description of when this hint will be shown. Example: 'The user has the key but hasn't unlocked the chest yet.'")
    messages: list[str] = Field(description="3 hints getting progressively more direct. Example: ['Check your inventory. The key is useful for unlocking things.', 'Look in the bedroom for something to use the key on.', 'Unlock the chest in the bedroom with the key.']")
