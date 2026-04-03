from pydantic import BaseModel

class Item(BaseModel):
    key: str
    short_description: str
    long_description: str
    is_openable: bool
    is_container: bool
    hidden_item_reveal_condition: str