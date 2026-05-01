from pydantic import BaseModel, Field

class CustomCommand(BaseModel):
    command: str = Field(description="the name of the command to execute. example: 'stab'")
    detailed_description: str = Field(description="the description of what the command does and how it works. example: \"'stab' can be used with any item, but only specific items do something (e.g. sword). If the user specifies an item to stab that isn't one of the objects that do something, respond with a generic 'you stab the __. It doesn't do anything.' If the user doens't specify anything to stab, respond with 'what do you want to stab?' If the user doesn't specify something to stab with, assume it's a sword.\"")
    custom_default_behavior: bool = Field(description="Whether or not the fallback should be custom or the game default - return null - for when no criteria are met for this command to do something. This will always be true if overriding a default command for custom behavior (e.g. eat or look), and it will usually be false for new, custom commands, but may be true if the user wants the default response if no conditions are met.")
