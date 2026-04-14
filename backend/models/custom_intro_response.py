from pydantic import BaseModel, Field

from backend.models.custom_intro_answer import CustomIntroAnswer


class CustomIntroResponse(BaseModel):
    yes_answer: str = Field(description='The game\'s response for when the user answers the intro question with "yes".')
    no_answer: str = Field(description='The game\'s response for when the user answers the intro question with "no".')
    custom_answers: list[CustomIntroAnswer]