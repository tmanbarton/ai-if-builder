import queue

from anthropic import Anthropic

system_message = """
You are a Java file generator with expertise in, using the if-engine Java library for creating interactive fiction games.
Your job is to take an input spec that has the user's interactive fiction game design and turn it into the backend of a
fully playable game using the if-engine Java library. The spec document will have the map, the items, custom commands,
default commands to override, puzzles, and more. You will first parse the document into a JSON object representing the
various parts of the game, then pass it on to agents to handle creating the Java files.
"""

def generator(q: queue.Queue):
    while True:
        message: str = q.get()
        if message is None:
            return
        yield message

def run_agent(q: queue.Queue, spec: str):
    messages = [{"role": "user", "content": spec}]

    q.put("event: status\ndata: Parsing specs\n\n")
    client = Anthropic()
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=system_message,
        messages=messages
    )

    q.put(None)
