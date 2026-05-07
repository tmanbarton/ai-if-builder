import asyncio
import queue
import sys
from pathlib import Path
from typing import Any
import threading

from mcp import StdioServerParameters, stdio_client, ClientSession
from mcp.types import CallToolResult


SERVER_PATH = str(Path(__file__).resolve().parent.parent / "mcp_server" / "search_docs_server.py")

_client = None
_client_session = None
_loop = asyncio.new_event_loop()
_loop_thread = threading.Thread(target=_loop.run_forever, daemon=True)
_loop_thread.start()

def search_docs(session_id: str, q: queue.Queue, tool_input: dict[str, Any]):
    queue_data: str = f"event: status\ndata: Fetching documentation... ({tool_input['question']})\n\n"
    q.put(queue_data)
    return asyncio.run_coroutine_threadsafe(query_embedding(tool_input["question"]), _loop).result()

async def query_embedding(query: str):
    global _client, _client_session

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[SERVER_PATH]
    )

    # Lazy load client session and manually enter stdio_client and ClientSession so they are open for the entire lifecycle of the agent. Exit when the agent loop is done
    if _client_session is None:
        _client = stdio_client(server_params)
        read, write = await _client.__aenter__()
        _client_session = ClientSession(read, write)
        await _client_session.__aenter__()
        await _client_session.initialize()
    result: CallToolResult = await _client_session.call_tool("search_docs", {"query": query})

    return result.content[0].text

async def _close():
    global _client, _client_session
    if _client_session is not None:
        await _client_session.__aexit__(None, None, None)
        await _client.__aexit__(None, None, None)
        _client_session = None
        _client = None

def close_mcp_server():
    asyncio.run_coroutine_threadsafe(_close(), _loop).result()
    _loop.call_soon_threadsafe(_loop.stop)
