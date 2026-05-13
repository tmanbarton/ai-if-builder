import queue
from typing import Any

from backend.tools.write_puzzles import execute_write


def write_custom_commands(session_id: str, q: queue.Queue, tool_input: dict[str, Any]):
    q.put("event: status\ndata: Writing code for custom commands...\n\n")

    execute_write(session_id, tool_input)
