import json
import queue
import uuid
from threading import Timer
from typing import Any

from anthropic import Anthropic

from backend.build_map import build_map
from backend.constants import CLAUDE_SONNET_MODEL
from backend.create_intro import create_intro
from backend.database import clear_data, fetch_all_files
from backend.game_scaffolding import initialize
from backend.tools.definitions import TOOL_DEFINITIONS, TOOL_HANDLERS
from backend.tools.search_docs import close_mcp_server

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
    # session id used as a key for files stored in sqlite db
    # session_id: str = "a9175fc0-c0fc-4a83-9607-00804b821dcb"
    session_id: str = str(uuid.uuid4())

    # 1. Write build.gradle and Game.java class to db, which are the same every time
    # 2. Call Claude API to extract map and any intro stuff if present to create those deterministically.
    # 3. Start agentic loop
    initialize(session_id)
    build_map(session_id, q, spec)
    create_intro(session_id, q, spec)

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
                result = handler(session_id, q, block.input)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })

        messages.append({"role": "user", "content": tool_results})

    files: list[Any] = fetch_all_files(session_id)
    for file in files:
        q.put(f"event: file\ndata: {json.dumps({'name': file[0], 'content': file[1]})}\n\n")

    # Send the session id as a different even type so the front end can use the session id for downloading the files
    q.put(f"event: session\ndata: {session_id}\n\n")
    q.put("event: status_done\ndata: Done\n\n")
    q.put(None)

    # Clean up after 15 minutes if the user doesn't download the files.
    # Delete files immediately if they do download.
    Timer(900, clean_up, args=[session_id]).start()

def clean_up(session_id: str):
    # Delete generated files once they've been sent to the frontend
    clear_data(session_id)
    close_mcp_server()
