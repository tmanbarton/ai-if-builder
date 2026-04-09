from pydantic import BaseModel, Field

from backend.models.custom_command import CustomCommand

class CustomCommands(BaseModel):
    custom_commands: list[CustomCommand]