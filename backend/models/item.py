from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str = Field(description="The unique name of the item. Used as a key to identify this item and for checking the user's input. Starts with a lowercase letter and words separated by spaces.")
    inventory_description: str
    location_description: str
    detailed_description: str
    aliases: list[str] = Field(default=list(), description="A list of possible names the user could identify this item as. e.g. item: parchment letter, name=letter, aliases=[paper, parchment]. And, if applicable, include plural and singular forms of aliases also.")
    location: str = Field(description="The location name this item is at.")
    is_openable: bool = False
    is_unlockable: bool = False
    is_container: bool = False
    hidden_item_reveal_condition: str | None = Field(default=None, description="If this item is a hidden item, this field is non-None. If the item is not hidden, this field is set to None. This is the description of what causes the hidden item to be revealed. Examples: When the user unlocks and opens the chest. When the user looks under the table the item becomse visible")
