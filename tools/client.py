import asyncio
import os
import sys
from typing import Dict, List

from mcp import ClientSession, StdioServerParameters, stdio_client

SERVER_NAME = "ai-mentor-research"
SERVER_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server.py")
TIMEOUT_SECONDS = 30


class MCPClient:
    def __init__(self):
        self.server_name = SERVER_NAME
        self.params = StdioServerParameters(command=sys.executable, args=[SERVER_SCRIPT])
        self.tools: List[Dict] = []
        self.error: str = ""
        self._discover()

    @property
    def tool_names(self) -> List[str]:
        return [tool["function"]["name"] for tool in self.tools]

    def _discover(self) -> None:
        try:
            self.tools = asyncio.run(self._list_tools())
        except Exception as e:
            self.tools = []
            self.error = f"{type(e).__name__}: {e}"

    async def _list_tools(self) -> List[Dict]:
        async with stdio_client(self.params) as (read, write):
            async with ClientSession(read, write, read_timeout_seconds=TIMEOUT_SECONDS) as session:
                await session.initialize()
                result = await session.list_tools()
                return [self._to_openai_schema(tool) for tool in result.tools]

    @staticmethod
    def _to_openai_schema(tool) -> Dict:
        return {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description or "",
                "parameters": tool.input_schema,
            },
        }

    def call_tool(self, name: str, arguments: Dict) -> str:
        return asyncio.run(self._call_tool(name, arguments))

    async def _call_tool(self, name: str, arguments: Dict) -> str:
        async with stdio_client(self.params) as (read, write):
            async with ClientSession(read, write, read_timeout_seconds=TIMEOUT_SECONDS) as session:
                await session.initialize()
                result = await session.call_tool(name, arguments)
                text = "\n".join(
                    block.text for block in result.content if getattr(block, "type", "") == "text"
                )
                if result.is_error:
                    return f"External tool '{name}' returned an error: {text}"
                return text
