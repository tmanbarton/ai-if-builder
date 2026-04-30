import json
import queue
from typing import Any

from anthropic import Anthropic

from backend.constants import CLAUDE_SONNET_MODEL
from backend.models.nondeterministic_fields import NondeterministicFields
from backend.models.puzzle import Puzzle
from backend.tools.definitions import CREATE_PUZZLES_AGENT_TOOLS, TOOL_HANDLERS

system_message = """
You're only job in life is to write Java code using the if-engine library to create puzzles for an interactive fiction game.
You are a skilled Java developer. You will receive a pre-parsed JSON object representing any puzzles in the game based on user specification.
To get information about the if-engine library, use the query_docs tool. First, analyze the puzzles one at a time and determine what questions need 
to be asked. Example puzzle: "The player finds a bottle in the kitchen location and, once they have the bottle, they can take the spilled grease from 
the garage (fill the bottle since you can't take the grease with your hands). The player can then put the grease on the door with the rusted 
hinges in the basement to open it and continue."
From that description you need to know:
- How to make an item contain another item (bottle holds grease). -> How do I make an item hold another item?
- Make an informed decision to determine valid and **simple** ways to get the grease on the door: "put grease on door", "drop grease" (while at the door location),
"grease door", "put grease on hinges", "grease hinges". 
- Determine how to alter the logic for the default commands and how add a custom command ("grease") -> How do I create new logic for a default command? 
and, How do I create a new command?
- How to change the state of the game when something happens, (put grease on the door, open the door, connect door to whatever is behind the door) ->
How do I change game state when a user runs a command?

Note: if there is a completely new command that the puzzle relies on, make sure it doesn't already exist. The create_custom_commands tool is called before this one 
and its job is to create custom commands that apply to the whole game. Puzzles could use commands like that.
"""

def create_puzzles(q: queue.Queue, tool_input: dict[str, Any]):
    """
    Sub-agent for writing Java code for game puzzles using the if-engine library.
    It has one tool available: query_docs. It loops, asking query_docs for info on the library and writing code until it determines it's done.
    :param q: Queue for sending status to SSE connection to show on frontend
    :param tool_input: JSON representing the game's puzzles which is just a detailed description of the puzzle and any custom commands it requires
    with a detailed description of how that command behaves.
    :return:
    """
    q.put('event: status\ndata: Creating puzzles...\n\n')
    puzzles_json: str = json.dumps(tool_input)
    messages = [{'role': 'user', 'content': [{'type': 'text', 'text': puzzles_json}]}]
    client = Anthropic()

    # Sub-agent loop
    while True:
        response = client.messages.parse(
            model=CLAUDE_SONNET_MODEL,
            max_tokens=16000,
            system=system_message,
            messages=messages,
            tools=CREATE_PUZZLES_AGENT_TOOLS
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            break

        # todo pull out into separate function since this is the same as in agent.run_agent
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                # Dispatch the tool using the tool_handler dict
                handler = TOOL_HANDLERS[block.name]
                result = handler(q, block.input)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })

        messages.append({"role": "user", "content": tool_results})


    # todo change response from NondeterministicFields to something else. The response is now actual Java code.
    #  Also could be Claude saying to use the query_docs tool
    response_data: NondeterministicFields = response.parsed_output
    puzzles: list[Puzzle] = response_data.puzzles
    a = 0