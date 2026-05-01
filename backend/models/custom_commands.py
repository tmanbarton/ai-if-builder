from pydantic import BaseModel

from backend.models.custom_command import CustomCommand


class CustomCommands(BaseModel):
    commands: list[CustomCommand]
