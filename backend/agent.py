import queue

from anthropic import Anthropic

from backend.build_map import build_map
from backend.models import game_model
from backend.models.game_model import GameModel

system_message = """
You are a Java file generator with expertise in, using the if-engine Java library for creating interactive fiction games.
Your job is to take an input spec that has the user's interactive fiction game design and turn it into the backend of a
fully playable game using the if-engine Java library. The spec document will have the map, the items, custom commands,
default commands to override, puzzles, and more. You will first parse the document into a JSON object representing the
various parts of the game, then pass it on to agents to handle creating the Java files.
**IMPORTANT** Do NOT populate descriptions. The interactive community is super touchy on the idea of AI-generated content.
Instead, insert placeholder text so the user can fill the descriptions themselves. (e.g. "Dungeon long description", "Sword detailed description"))
"""

def generator(q: queue.Queue):
    while True:
        message: str = q.get()
        if message is None:
            return
        yield message

def run_agent(q: queue.Queue, spec: str):
    build_map(q, spec)

    # messages = [{"role": "user", "content": spec}]
    #
    # q.put("event: status\ndata: Parsing specs\n\n")
    # client = Anthropic()
    # response = client.messages.parse(
    #     model="claude-sonnet-4-6",
    #     max_tokens=16000,
    #     system=system_message,
    #     messages=messages,
    #     output_format=GameModel
    # )
    #
    # messages.append({"role": "agent", "content": response.content[0].text})


    q.put(None)
