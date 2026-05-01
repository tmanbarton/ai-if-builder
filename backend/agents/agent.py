import queue

from anthropic import Anthropic

from backend.build_map import build_map
from backend.constants import CLAUDE_SONNET_MODEL
from backend.create_intro import create_intro
from backend.database import clear_data
from backend.tools.definitions import TOOL_DEFINITIONS, TOOL_HANDLERS

system_message = """
You are a Java file generator with expertise in, using the if-engine Java library for creating interactive fiction games. 
Your job is to take an input spec that has the user's interactive fiction game design and turn it into the backend of a 
fully playable game using the if-engine Java library. The spec document will have the map, the items (ignore these, they're already processed), 
custom commands, default commands to override, puzzles, and more. You will first parse the document into a JSON object representing the 
various parts of the game, then pass it on to agents to handle creating the Java files.
"""

def generator(q: queue.Queue):
    while True:
        message: str = q.get()
        if message is None:
            return
        yield message

def run_agent(q: queue.Queue, spec: str):
    # First call Claude API to extract map and create it deterministically. Start agentic loop after.
    build_map(q, spec)
    create_intro(q, spec)

    messages = [{"role": "user", "content": [{"type": "text", "text": spec}]}]
    client = Anthropic()
    while True:
        response = client.messages.create(
            model=CLAUDE_SONNET_MODEL,
            system=system_message,
            messages=messages,
            tools=TOOL_DEFINITIONS,
            max_tokens=16000
        )

        messages.append({"role": "assistant", "content": response.content})

        # If Claude didn't say to use a tool, it's done
        if response.stop_reason != "tool_use":
            break

        # Otherwise find and execute each specified tool
        tool_results: list[dict] = []
        for block in response.content:
            if block.type == "tool_use":
                # Dispatch tool using the tool_handler dict
                handler = TOOL_HANDLERS[block.name]
                result = handler(q, block.input)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })

        messages.append({"role": "user", "content": tool_results})

    # Delete generated files before sending final result to frontend.
    clear_data()

    q.put(None)
