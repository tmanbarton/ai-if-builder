import asyncio
import queue
import sys
from typing import Any

from mcp import StdioServerParameters, stdio_client, ClientSession
from mcp.types import CallToolResult

def search_docs(q: queue.Queue, tool_input: dict[str, Any]):
    q.put(f"event: status\ndata: Fetching documentation...\n({tool_input['question']})\n\n")
    return asyncio.run(query_embedding(tool_input["question"]))

async def query_embedding(query: str):
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["backend/mcp_server/search_docs_server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result: CallToolResult = await session.call_tool("search_docs", {"query": query})

    return result.content[0].text
