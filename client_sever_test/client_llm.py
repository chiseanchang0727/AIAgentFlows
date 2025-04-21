"""
User chat with LLM to use the tools
"""
import logging
import json
import asyncio
import os
from typing import Optional
from openai import OpenAI
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from dotenv import load_dotenv

logger = logging.getLogger("mcp_client")
logger.setLevel(logging.DEBUG)
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')


class MCPClient:
    def __init__(self):
        self.session = Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.client = OpenAI(api_key=api_key, model='gpt-4o', temperature=0.0, max_tokens=2000)


    async def connect_to_sever(self):
        print('we here')
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
        stdio, write = await self.exit_stack.enter_async_context(stdio_client(sever_params))

        """
        1. ClientSession(...) creates a session object that communicates over the stdio transport
        2. It’s an async context manager, which:
            - Does setup in __aenter__()
            - Requires cleanup in __aexit__() (e.g. closing the connection)
        """
        self.session = await self.exit_stack.enter_async_context(ClientSession(stdio, write))

        await self.session.initialize()

    # Interaction between user and mcp sever
    async def process_query(self, query:str) -> str:
        system_prompt = (
            "You are a helpful assistant."
            "You have the function of online search. "
            "Please MUST call web_search tool to search the Internet content before answering."
            "Please do not lose the user's question information when searching,"
            "and try to maintain the completeness of the question content as much as possible."
            "When there is a date related question in the user's question," 
            "please use the search function directly to search and PROHIBIT inserting specific time."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]

        # Get all tools
        response = await self.session.list_tools()
        
        # Describe the tools
        available_tools = [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            }
        } for tool in response.tools]
        
        # Add the tools to the messages
        response = self.client.chat.completions.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-4o'),
            messages=messages,
            tools=available_tools
        )
        
        content = response.choices[0]
        if content.finish_reason == 'tool_calls':
            # If LLM decide to call tools, parse and pass the info to the session
            tool_call = content.message.tool_calls[0]
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            
            result = await self.session.call_tool(tool_name, tool_args)
            print(f"\n\n[Calling tool {tool_name} with args {tool_args}]\n\n")
            
            messages.append(content.message.model_dump())
            messages.append({
                'role': 'tool',
                'content': result.content[0].text,
                'tool_call_id': tool_call.id
            })
            
            # Pass the integrated the tool result into the messages to LLM
            response = self.client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL"),
                messages=messages,
            )
            
            return response.choices[0].message.content
        
        return content.message.content