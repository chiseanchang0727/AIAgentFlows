from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP(name="Prompt test App")

@mcp.prompt()
def review_the_article(input: str) -> str:
    return f"Review the following article, list out the key subject and concepts: \n\n{input}"


@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I am seeing this error."),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?")
    ]


@mcp.list_prompts()
def list_prompts(input:str):
    pass