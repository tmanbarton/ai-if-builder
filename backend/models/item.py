from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str = Field(description="The unique name of the item. Used as a key to identify this item.")
    inventory_description: str
    location_description: str
    detailed_description: str
    location: str = Field(description="The location name this item is at.")
    is_openable: bool
    is_unlockable: bool
    is_container: bool
    hidden_item_reveal_condition: str | None = Field(description="If this item is a hidden item, this field is non-None. If the item is not hidden, this field is set to None. This is the description of what causes the hidden item to be revealed. Examples: When the user unlocks and opens the chest. When the user looks under the table the item becomse visible")
