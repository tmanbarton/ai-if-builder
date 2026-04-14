import queue

from anthropic import Anthropic

system_message = 'todo'

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
    response = client.messages

# skip intro
# with intro responses - yes no
# with intro message