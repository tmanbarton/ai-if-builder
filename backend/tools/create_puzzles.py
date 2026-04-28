import json
import queue
from typing import Any

from anthropic import Anthropic

from backend.models.nondeterministic_fields import NondeterministicFields
from backend.models.puzzle import Puzzle

system_message = """
This tool takes a specification defining an interactive fiction game provided by the user and pulls out all of the puzzles into JSON.
This is part of a process in generating a working backend for the IF spec provided. This is important because puzzles are generally ambiguous
and can't be created deterministically. Your job is to determine what the puzzles are in the spec and parse them into JSON with the only
necessary field being a DETAILED DESCRIPTION of ONLY THE RELEVANT INFORMATION of the puzzle. This is important so future Claudes don't have any
ambiguity in the actual implementation of the puzzles.
For example, if the spec says "The player needs to find three numbers in three locations (Waterfall: 4, Garage: 58, Building: 33).
They have the numbers to unlock a number lock at the bedroom location with the order '58, 33, 4'. The lock is on a chest under the bed.
When it's opened, a notebook and pictures are revealed."
You would make the description something like: "There is a number lock that's locking a chest in the bedroom location. The player unlocks the lock with three
numbers in this order: '58, 33, 4'. When the chest is opened, it reveals two hidden items: a notebook and pictures."
Note how the description doesn't include information about where the numbers are located since the number lock doesn't care about the
location of the numbers, just the number order. The description gives only the information needed to create the puzzle.
"""

def create_puzzles(q: queue.Queue, tool_input: dict[str, Any]):
    q.put('event: status\ndata: Analyzing puzzles...\n\n')
    puzzles_json: str = json.dumps(tool_input)
    messages = [{'role': 'user', 'content': [{'type': 'text', 'text': puzzles_json}]}]
    client = Anthropic()
    response = client.messages.parse(
        model=CLAUDE_SONNET_MODEL,
        max_tokens=16000,
        system=system_message,
        messages=messages,
        output_format=NondeterministicFields
    )

    response_data: NondeterministicFields = response.parsed_output
    puzzles: list[Puzzle] = response_data.puzzles
    a = 0