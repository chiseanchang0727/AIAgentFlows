import asyncio
import logging

from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters

# Setup logger
logger = logging.getLogger("mcp_client")
# Sets the logging level to DEBUG, so this logger will capture all messages at DEBUG level and above (i.e., DEBUG, INFO, WARNING, ERROR, CRITICAL).
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)

# Server parameters for running the mcp server
logger.info("Start calling mcp server")
server_params = StdioServerParameters(
    command='uv',
    args=['run', 'web_search.py'],
    # env=None  # Use current environment
)
logger.info("Finished preparing server parameters")

async def main():
    try:
        # Create the stdio client for mcp server
        async with stdio_client(server_params) as (stdio, write):
            logger.info("Connected to MCP server via stdio")

            # Create session
            async with ClientSession(stdio, write) as session:
                # Initialize client session
                await session.initialize()
                logger.info("Client session initialized")

                # List the tools
                response = await session.list_tools()
                # logger.info(f"Available tools: {response}")

                # Example tool call (commented out)
                response = await session.call_tool('web_search', {'input': 'current sp500 index value'})
                logger.info(f"Tool response: {response}")
    except Exception as e:
        logger.exception("An error occurred during MCP session")

if __name__ == '__main__':
    asyncio.run(main())
