from pydantic import BaseModel, Field

from backend.models.connection import Connection
from backend.models.item import Item
from backend.models.location import Location
from backend.models.custom_command import CustomCommand
from backend.models.custom_intro_response import CustomIntroResponse
from backend.models.hint import Hint
from backend.models.overridden_command import OverriddenCommand
from backend.models.puzzle import Puzzle


class GameModel(BaseModel):
    locations: list[Location]
    connections: list[Connection] = Field(description="All connections that connect the locations to make the nodes and edges in the directed graph.")
    items: list[Item]
    puzzles: list[Puzzle]
    custom_commands: list[CustomCommand]
    overridden_commands: list[OverriddenCommand]
    hints: list[Hint]
    custom_intro_response: CustomIntroResponse
    should_skip_intro: bool = Field(description="Whether or not the game should skip the intro message and go straight into the game.")
    intro_message: str = Field(description="The intro message for the game.")