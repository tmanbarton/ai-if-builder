from pydantic import BaseModel, Field


class CustomIntroAnswer(BaseModel):
    user_answer: str = Field(description="the exact name of the user answer. Examples: 'easy', 'hard'")
    response: str = Field(description="The game response to the user's answer. Examples: 'You are now playing in easy mode.', 'You are now playing in hard mode.'")
