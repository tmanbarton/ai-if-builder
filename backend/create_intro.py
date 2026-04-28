import queue
import uuid
from io import StringIO

from anthropic import Anthropic

from backend.database import insert_file
from backend.models.custom_intro_answer import CustomIntroAnswer
from backend.models.custom_intro_response import CustomIntroResponse
from backend.models.intro import Intro

system_message = '''
You're only job in life is to extract information from a user-provided spec that defines an interactive fiction.
You will extract information about the introduction. There may or may not be anything specified, but if there is, there are several things that may be specified:
The answer to a yes/no intro question, the game introduction message, completely custom intro info (non-yes/no answer options or custom behavior on
answering the intro question).
If info on the intro is present, there won't be any particular format it will be presented in. You will have to use your best judgement to determine 
what is intro information and if it's present at all.
Note: DO NOT try to fill in the response with actual text, use placeholder text like "yes response" or "game intro". The user will complete the full responses themselves.
'''

def create_intro(q: queue.Queue, spec: str):
    """
    Sends the spec input to Claude for it to extract any information on the intro to the game into JSON. If any exist, deterministically create
    intro information based on the JSON. That information can be:\n
    - Should the intro be skipped
    - The specific response for when the user answers yes or no to the initial question
    - The actual game intro
    :param q: Queue for sending SSE events to the front end. Automatically sends the message when an element is added
    :param spec: Game spec that the user submitted to send to Claude.
    """
    q.put('event: status\ndata: Creating intro...\n\n')

    messages = [{'role': 'user', 'content': spec}]
    client = Anthropic()
    response = client.messages.parse(
        model=CLAUDE_SONNET_MODEL,
        max_tokens=16000,
        system=system_message,
        messages=messages,
        output_format=Intro
    )

    intro: Intro = response.parsed_output
    game_intro: str = intro.game_intro
    should_skip_intro: bool = intro.should_skip_intro
    intro_response: CustomIntroResponse = intro.intro_response
    intro_answer: list[CustomIntroAnswer] = intro.intro_answer

    write_files(should_skip_intro, game_intro, intro_response, intro_answer)
    # todo what to do for when intro answer is not None? Need to call Claude and have it reference the docs.

    q.put('event: status_done\ndata: Intro created.\n\n')

def write_files(should_skip_intro: bool, game_intro: str | None, intro_response: CustomIntroResponse, intro_answer: list[CustomIntroAnswer],
                db_name: str = 'database.db'):
    session_id: str = str(uuid.uuid4())

    constants_buf: StringIO = StringIO()
    if should_skip_intro:
        constants_buf.write('.skipIntro()')

    if game_intro is not None:
        constants_buf.write(f'.gameIntro("{game_intro}")')

    if intro_response.yes_answer and intro_response.no_answer:
        constants_buf.write(f'.withIntroResponse("{intro_response.yes_answer}", "{intro_response.no_answer}")')

    insert_file(session_id, 'intro-info.txt', constants_buf.getvalue(), db_name)

    return session_id
    # .skipIntro()
    # .withIntroResponse(yesAnswer, noAnswer)
    # .withGameIntro(introMessage)

# skip intro
# with intro responses - yes no
# with game intro