from pydantic import BaseModel, Field

from backend.models.custom_intro_answer import CustomIntroAnswer


class CustomIntroResponse(BaseModel):
    yes_answer: str = Field(description="The response when the user answers 'yes'.")
    no_answer: str = Field(description="The response when the user answers 'no'.")
    custom_answers: list[CustomIntroAnswer]