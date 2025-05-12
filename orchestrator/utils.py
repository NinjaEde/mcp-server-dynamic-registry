import asyncio
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os
import traceback

def get_kunde_by_key(api_key: str, kunden: dict):
    for kunde, info in kunden.items():
        if info["api_key"] == api_key:
            return kunde, info
    return None, None

async def call_mcp_tool(server_script_path, tool, params, timeout=10):
    try:
        async with AsyncExitStack() as stack:
            server_params = StdioServerParameters(command="python", args=[server_script_path], env=os.environ.copy())
            stdio = await stack.enter_async_context(stdio_client(server_params))
            session = await stack.enter_async_context(ClientSession(*stdio))
            await session.initialize()
            result = await session.call_tool(tool, params)
            return result
    except Exception as e:
        tb = traceback.format_exc()
        return f"Exception: {e}\nTraceback:\n{tb}"

