from pydantic import BaseModel, Field


class CustomIntroResponse(BaseModel):
    yes_answer: str = Field(description='The game\'s response for when the user answers the intro question with "yes".')
    no_answer: str = Field(description='The game\'s response for when the user answers the intro question with "no".')
