import queue
import sqlite3
from typing import Any

from backend.db_helpers import append, upsert, insert


def write_puzzles(session_id: str, q: queue.Queue, tool_input: dict[str, Any]):
    q.put("event: status\ndata: Writing code for puzzles...\n\n")
    execute_write(session_id, tool_input)

def execute_write(session_id: str, tool_input: dict[str, Any]):
    for file in tool_input["files"]:
        db_operation_type = file["db_operation_type"]
        match db_operation_type.lower():
            case "insert":
                try:
                    insert(session_id, file["file_name"], file["code"])
                except sqlite3.IntegrityError:
                    return f"The file {file['file_name']} already exists. Did you mean to update instead of insert?"
            case "update":
                upsert(session_id, file["file_name"], file["code"])
            case "append":
                append(session_id, file["file_name"], file["code"])
