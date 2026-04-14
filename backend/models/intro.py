from pydantic import BaseModel, Field

from backend.models.custom_intro_answer import CustomIntroAnswer
from backend.models.custom_intro_response import CustomIntroResponse


class Intro(BaseModel):
    game_intro: str = Field(description='The game introduction. This is what sets up the game story. It goes after the user answers the intro '
                                        'question and comes before the first location\'s description.')
    should_skip_intro: bool = Field(description='Whether or not to skip the game introduction and go straight to the first location\'s description.')
    intro_response: CustomIntroResponse
    intro_answer: list[CustomIntroAnswer]