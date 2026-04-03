from pydantic import BaseModel

class CustomIntroAnswer(BaseModel):
    user_answer: str
    response: str