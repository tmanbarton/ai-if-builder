from pydantic import BaseModel, Field


class Puzzle(BaseModel):
    detailed_description: str = Field(description="The description of the puzzle. Detailed info on how the puzzle works - what the flow is, what items and commands and anything else is involved. This information is vital for determining what custom features to add and what custom logic to add. It is critical to provide enough information to avoid ambiguity for future Claudes that write code.")
