from pydantic import BaseModel

class OverriddenCommand(BaseModel):
    command: str
    description: str