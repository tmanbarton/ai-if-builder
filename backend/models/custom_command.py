from pydantic import BaseModel

class CustomCommand(BaseModel):
    command: str
    description: str
    custom_default_behavior: str | None