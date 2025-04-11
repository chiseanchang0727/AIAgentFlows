"""
User chat with LLM to use the tools
"""

import json
import asyncio
import os
from typing import Optional
from openai import OpenAI
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')


class MCPClient:
    def __init__(self):
        self.session = Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack
        self.client = OpenAI()


    async def connect_to_sever(self):
        sever_params = StdioServerParameters(
            command='uv',
            args=['run', 'web_search.py'],
            env=None
        )

        """
        1. Launch a subprocess via stdio_client(...)
        2. Enter its async with context safely via exit_stack
        3. Store the transport (connection handle) in stdio_transport
        4. It will be auto-cleaned when self.exit_stack is closed
        """
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(sever_params))

        stdio, write = stdio_transport

        self.session = await self.exit_stack.enter_async_context(ClientSession(stdio, write))

        await self.session.initialize()