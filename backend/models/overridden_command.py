from pydantic import BaseModel, Field


class OverriddenCommand(BaseModel):
    command: str = Field(description="the name of the default command to execute. Example: 'eat'. These can only be commands that are already built into the game.")
    description: str = Field(description="The description of how the command should work and what it does. Example: 'eat' is overridden so that when the user says to 'eat pie' a response of 'Yum, tasty pie' is sent. Otherwise, use the default functionality.'")
