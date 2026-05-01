import queue
from typing import Any


def write_custom_commands(q: queue.Queue, tool_input: dict[str, Any]):
    q.put("event: status\ndata: TODO Writing code for custom commands...\n\n")
