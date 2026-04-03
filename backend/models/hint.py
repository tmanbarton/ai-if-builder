from pydantic import BaseModel

class Hint(BaseModel):
    condition: str
    messages: list[str]