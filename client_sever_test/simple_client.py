import asyncio

from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters

# sever paramters for running the mcp sever
sever_params = StdioServerParameters(
    command='uv',
    args=['run', 'C:/Users/TWCC752671/Sean/git/AIAgentFlows/client_sever_test/web_search.py'],
    #env=None # use current enviornment
)


async def main():
    # create the stdio client for mcp sever
    async with stdio_client(sever_params) as (stdio, write):

        # create session
        async with ClientSession(stdio, write) as session:
            # initialize client session
            await session.initialize()

            # list the tools
            response = await session.list_tools()
            print(response)

            # call tools
            # response = await session.call_tool('web_search', {'query': 'current sp500 index value'})
            # print(response)

if __name__ == '__main__':
    asyncio.run(main())