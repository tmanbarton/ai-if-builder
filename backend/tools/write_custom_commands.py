import queue
from typing import Any

from backend.database import insert_file


def write_custom_commands(session_id: str, q: queue.Queue, tool_input: dict[str, Any]):
    q.put("event: status\ndata: TODO Writing code for custom commands...\n\n")

    for file in tool_input["files"]:
        insert_file(session_id, file["file_name"], file["code"])
    return session_id
