from pydantic import BaseModel

from backend.models.custom_intro_answer import CustomIntroAnswer


class CustomIntroResponse(BaseModel):
    yes_answer: str
    no_answer: str
    custom_answers: list[CustomIntroAnswer]