from pydantic import BaseModel

from backend.models.puzzle import Puzzle


class Puzzles(BaseModel):
    puzzles: list[Puzzle]
