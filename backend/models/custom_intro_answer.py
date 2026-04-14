from pydantic import BaseModel, Field


class CustomIntroAnswer(BaseModel):
    user_answer: str = Field(description="the exact name of the user answer. Examples: 'easy', 'hard'. Anything other than 'yes' and 'no' should go "
                                         "here, if the user specified, OR if there is custom behavior when answering yes/no.")
    response: str = Field(description="The game response to the user's answer. Examples: 'You are now playing in easy mode.', 'You are now playing in hard mode.'")
    description: str = Field(default=None, description='Detailed description of what happens when the user answers the question with this answer. '
                                                       'Only set this if something more complicated happens than sending a unique message. For '
                                                       'example: Question is "Easy or had mode?" User enters "hard". Description is. "Set the game '
                                                       'mode to hard and update the starting location to the cave." If nothing extra happens besides '
                                                       'a unique message, this field is set to None.')
