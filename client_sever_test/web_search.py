import httpx
from mcp.server import FastMCP

app = FastMCP('web-search')


# openai web search
@app.tool()
async def web_search(query: str) -> str:
    async with httpx.AsyncClient() as client:
        response = client.responses.create(
            model='gpt-4o',
            tools=[{"type": "web_search_preview"}],
            input=query
        )

        output = response.output_text




        return output