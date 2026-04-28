from pydantic import BaseModel

from backend.models.custom_command import CustomCommand
from backend.models.hint import Hint
from backend.models.puzzle import Puzzle

class NondeterministicFields(BaseModel):
    puzzles: list[Puzzle]
    custom_commands: list[CustomCommand]
    hints: list[Hint]
    # todo maybe Interactions for scenery objects?