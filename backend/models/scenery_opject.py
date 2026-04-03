from pydantic import BaseModel

class SceneryObject(BaseModel):
    key: str | None = None
