from pydantic import BaseModel, Field


class Item(BaseModel):
    key: str = Field(description="The unique name of the item. Used as a key to identify this item.")
    inventory_description: str = Field(description="The short description of the item for when the user is viewing their inventory. Example: sword: 'A shiny sword'")
    location_description: str = Field(description="The longer description of the item for when the user is viewing a location with an item at it. Example: sword: 'There's a shiny sword here.'")
    detailed_description: str = Field(description="The long, detailed description for when the user inspects the item. Example: key: 'This here is a fine-looking sword. Modern and engraved on the blade with a mountain range and polished to a silver shine so you can see your own reflection in it.'")
    location: str = Field(description="The location key this item starts at.")
    is_openable: bool = Field(description="Whether or not the item is openable.")
    is_unlockable: bool = Field(description="Whether or not the item is unlockable.")
    is_container: bool = Field(description="Whether or not the item is a container.")
    hidden_item_reveal_condition: str | None = Field(description="If this item is a hidden item, this field is non-None. If the item is not hidden, this field is set to None. This is the description of what causes the hidden item to be revealed. Examples: When the user unlocks and opens the chest. When the user looks under the table the item becomse visible")
