from pydantic import BaseModel

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
    connections: list[Connection]
    items: list[Item]
    puzzles: list[Puzzle]
    custom_commands: list[CustomCommand]
    overridden_commands: list[OverriddenCommand]
    hints: list[Hint]
    custom_intro_response: CustomIntroResponse
    should_skip_intro: bool
    intro_message: str